import torch
from torch import nn
from nlpx.model import TextCNN, RNNAttention
from transformers import AutoModel, BertConfig, ErnieConfig, AutoTokenizer, AutoConfig


class TokenClassifier(nn.Module):

    def __init__(self, backbone, classifier, device, max_length: int):
        super().__init__()
        self.backbone = backbone
        self.classifier = classifier
        self.device = device
        self.max_length = max_length

    def forward(self, tokenizies: dict):
        tokenizies = {k: v.to(self.device) for k, v in tokenizies.items()}
        outputs = self.backbone(**tokenizies, output_hidden_states=True)
        return self.classifier(outputs.last_hidden_state[:, 1:])  # 除去[cls]的

    def fit(self, inputs, labels: torch.Tensor):
        logits = self.forward(inputs)
        return nn.functional.cross_entropy(logits, labels), logits


class AutoCNNTokenClassifier(TokenClassifier):

    def __init__(self, pretrained_path, num_classes: int, device, max_length: int = 256, config = None):
        config = config or AutoConfig.from_pretrained(pretrained_path)
        backbone = AutoModel.from_pretrained(pretrained_path)
        classifier = TextCNN(embed_dim=config.hidden_size, out_features=num_classes)
        for param in backbone.parameters():
            param.requires_grad_(False)
        super().__init__(backbone, classifier, device, max_length)

        
class BertCNNTokenClassifier(AutoCNNTokenClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
        config = BertConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, device, max_length, config)


class ErnieCNNTokenClassifier(AutoCNNTokenClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
        config = ErnieConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, device, max_length, config)


class AutoRNNAttentionTokenClassifier(TokenClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256, config = None):
        config = config or AutoConfig.from_pretrained(pretrained_path)
        bert = AutoModel.from_pretrained(pretrained_path)
        classifier = RNNAttention(embed_dim=config.hidden_size, out_features=num_classes)
        for param in bert.parameters():
            param.requires_grad_(False)
        super().__init__(bert, classifier, device, max_length)


class BertRNNAttentionTokenClassifier(AutoRNNAttentionTokenClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
        config = BertConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, device, max_length, config)


class ErnieRNNAttentionTokenClassifier(AutoRNNAttentionTokenClassifier):

    def __init__(self, pretrained_path, num_classes: int, device, max_length: int = 256):
        config = ErnieConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, device, max_length, config)


# class ModernBertCNNTokenClassifier(AutoCNNTokenClassifier):

#     def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
#         config = ModernBertConfig.from_pretrained(pretrained_path)
#         super().__init__(pretrained_path, num_classes, device, max_length, config)


# class ModernBertRNNAttentionTokenClassifier(AutoRNNAttentionTokenClassifier):

#     def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
#         config = ModernBertConfig.from_pretrained(pretrained_path)
#         super().__init__(pretrained_path, num_classes, device, max_length, config)


class TextClassifier(TokenClassifier):

    def __init__(self, pretrained_path, backbone, classifier, device, max_length: int):
        super().__init__(backbone, classifier, device, max_length)
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_path)

    def forward(self, texts):
        tokenizies = self.tokenizer.batch_encode_plus(texts,
                                                max_length=self.max_length,
                                                padding='max_length',
                                                truncation=True,
                                                return_token_type_ids=False,
                                                return_attention_mask=True,
                                                return_tensors='pt')
        return super().forward(tokenizies)
    

class AutoCNNTextClassifier(TextClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256, config = None):
        config = config or AutoConfig.from_pretrained(pretrained_path)
        backbone = AutoModel.from_pretrained(pretrained_path)
        classifier = TextCNN(embed_dim=config.hidden_size, out_features=num_classes)
        for param in backbone.parameters():
            param.requires_grad_(False)
        super().__init__(pretrained_path, backbone, classifier, device, max_length)
    

class BertCNNTextClassifier(AutoCNNTextClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
        config = BertConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, device, max_length, config)


class ErnieCNNTextClassifier(AutoCNNTextClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
        config = ErnieConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, device, max_length, config)


class AutoRNNAttentionTextClassifier(TextClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256, config = None):
        config = config or AutoConfig.from_pretrained(pretrained_path)
        backbone = AutoModel.from_pretrained(pretrained_path)
        classifier = RNNAttention(embed_dim=config.hidden_size, out_features=num_classes)
        for param in backbone.parameters():
            param.requires_grad_(False)
        super().__init__(pretrained_path, backbone, classifier, device, max_length)


class BertRNNAttentionTextClassifier(AutoRNNAttentionTextClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
        config = BertConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, device, max_length, config)


class ErnieRNNAttentionTextClassifier(AutoRNNAttentionTextClassifier):

    def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
        config = ErnieConfig.from_pretrained(pretrained_path)
        super().__init__(pretrained_path, num_classes, max_length, config)


# 需要 transformers>=4.48.3
# class ModernBertCNNTextClassifier(AutoCNNTextClassifier):

#     def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
#         config = ModernBertConfig.from_pretrained(pretrained_path)
#         super().__init__(pretrained_path, num_classes, device, max_length, config)


# class ModernBertRNNAttentionTextClassifier(AutoRNNAttentionTextClassifier):

#     def __init__(self, pretrained_path, num_classes, device, max_length: int = 256):
#         config = ModernBertConfig.from_pretrained(pretrained_path)
#         super().__init__(pretrained_path, num_classes, device, max_length, config)
