"""Gender bias predictor script"""

import csv
import html
import regex
# BiEncoderRankerAgent ranks the semantic similarity between the textual input and about/to/as
# gender bias classes defined by the dot product of their bi-encoder phrase vector representations
from parlai.agents.bert_ranker.bi_encoder_ranker import BiEncoderRankerAgent
import torch.nn.functional as F
# utils are utilities from the ParlAI MDGender task
import parlai.tasks.md_gender.utils as gender_utils
# validate is an assertion that ensures that the observation dictionary is valid
from parlai.core.worlds import validate
# ParlaiParser produces ParlAI option objects
from parlai.core.params import ParlaiParser

HASHTAG_CHARS = (r"\p{L}\p{M}\p{Nd}_\u200c\u200d\ua67e\u05be\u05f3\u05f4\uff5e\u301c\u309b\u309c"
                 r"\u30a0\u30fb\u3003\u0f0b\u0f0c\u00b7")

parser = ParlaiParser(False, False) # don't initialize the default ParlAI package + model arguments
parser.set_params(model='bert_ranker/bi_encoder_ranker', model_file='./models/md_gender/model')
opt = parser.parse_args([])
# https://github.com/facebookresearch/ParlAI/blob/main/parlai/core/torch_ranker_agent.py#L530
opt['return_cand_scores'] = True # receive class probabilities
model = BiEncoderRankerAgent(opt)

# https://github.com/facebookresearch/ParlAI/blob/7506a84e00e0ba526dca01b8aea97d009c91fa50/parlai/tasks/md_gender/worlds.py#L55
def predict_gender_bias(text):
    """Predict the gender bias of text"""
    # SELF (as) prediction
    self_observation = {'text': text, 'label_candidates': gender_utils.SELF_CANDS,
            'episode_done': True} # episode_done marks the end of an episode (a conversation)
    model.observe(validate(self_observation))
    self_action = model.act()
    self_prediction = zip(self_action['text_candidates'],
            F.softmax(self_action['sorted_scores']).tolist())

    # PARTNER (to) prediction
    partner_observation = {'text': text, 'label_candidates': gender_utils.PARTNER_CANDS,
            'episode_done': True}
    model.observe(validate(partner_observation))
    partner_action = model.act()
    partner_prediction = zip(partner_action['text_candidates'],
            F.softmax(partner_action['sorted_scores']).tolist())

    # ABOUT prediction
    about_observation = {'text': text, 'label_candidates': gender_utils.ABOUT_CANDS,
            'episode_done': True}
    model.observe(validate(about_observation))
    about_action = model.act()
    about_prediction = zip(about_action['text_candidates'],
            F.softmax(about_action['sorted_scores']).tolist())

    return self_prediction, partner_prediction, about_prediction

with open("tweets.csv", encoding="utf8") as t, open("predictions.csv", "w", encoding="utf8") as p:
    reader = csv.DictReader(t)
    writer = csv.DictWriter(p, fieldnames=(reader.fieldnames +
        [cand for axis in list(gender_utils.ALL_CANDS.values()) for cand in axis]))
    writer.writeheader()
    for row in reader:
        row["tweet"] = regex.sub(r"https?://t\.co/[a-zA-Z0-9]+",
                "", row["tweet"])

        row["tweet"] = regex.sub(r"(?:([^\w!#$%&*@＠]|^)|(?:^|[^\w+~.-])(?:rt|rT|Rt|RT):?)[@＠]"
                r"(\w{1,20}(?:/[a-zA-Z][\w-]{0,24})?)",
                r"\1\2", row["tweet"])

        row["tweet"] = regex.sub(r"(^|\ufe0e|\ufe0f|[^&" +
                HASHTAG_CHARS +
                r"])[#＃]((?!\ufe0f|\u20e3)[" +
                HASHTAG_CHARS +
                r"]*[\p{L}\p{M}][" +
                HASHTAG_CHARS +
                r"]*)",
                r"\1\2", row["tweet"])

        row["tweet"] = regex.sub(r"\n+",
                "\n", row["tweet"])

        row["tweet"] = regex.sub(r"\s+",
                " ", row["tweet"]).strip()

        row["tweet"] = html.unescape(row["tweet"])

        row.update(
                {k: v for axis in predict_gender_bias(row["tweet"]) for k, v in tuple(axis)})

        writer.writerow(row)
