from metaml.meta_models.metadata import MetaData, Supports, ModelTag, ModelTypeEnum
from metaml.meta_models.names import ClassifierName


metadata = MetaData(
    model_name=ClassifierName.nlp_sequence_classifier,
    model_type={ModelTypeEnum.deep_learning},
    tags={ModelTag.classifier, ModelTag.nlp},
    description="The NLP Sequence Classifier is an interface to Hugging Face's Transformers, designed to simplify and optimize text classification tasks. Leveraging pre-trained models from the Transformers library, this classifier aims to offer state-of-the-art performance in natural language understanding.",
    advantages=[
        "Leverages Pre-trained Models: By utilizing the pre-trained models from Hugging Face's extensive library, the NLP Sequence Classifier offers a quick and powerful way to benefit from the latest advancements in NLP without the need for extensive data or computational resources.",
        "Ease of Use: The wrapper simplifies the application of complex transformer-based models into text classification tasks, making it easier for developers to integrate advanced NLP functionalities into their applications.",
        "Highly Versatile: Given the underlying architecture, the NLP Sequence Classifier can be adapted to various text classification problems ranging from sentiment analysis to topic classification, providing high-quality results across a wide array of use-cases.",
    ],
    disadvantages=[
        "Computational Overhead: Utilizing transformer models generally comes with high computational costs in terms of memory and processing power, especially for large datasets or complex architectures.",
        "Lack of Interpretability: Transformer models, being highly complex, do not offer straightforward ways to interpret their decisions, making them less ideal for applications where model interpretability is crucial.",
        "Dependence on Pre-trained Models: While leveraging pre-trained models is an advantage in terms of performance and speed, it may limit customization and adaptation to highly specific or nuanced tasks that require training from scratch.",
    ],
    prime=["model"],
    display_name="NLP Sequence Classifier",
    supports=Supports(probabilities=True, feature_importances=False),
)
