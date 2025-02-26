from enum import Enum

class Capacity(str, Enum):
    # General Purpose
    SCRAPER = "SCRAPER"
    CRAWLER = "CRAWLER"
    EXTRACTOR = "EXTRACTOR"
    FORMATTER = "FORMATTER"
    SUMMARIZER = "SUMMARIZER"
    TRANSLATOR = "TRANSLATOR"
    DATA_CLEANER = "DATA_CLEANER"
    DATA_VALIDATOR = "DATA_VALIDATOR"
    DATA_INDEXER = "DATA_INDEXER"
    DATA_BROKER = "DATA_BROKER"
    OPTIMIZER = "OPTIMIZER"
    SIMULATOR = "SIMULATOR"
    CLASSIFIER = "CLASSIFIER"
    RECOMMENDER = "RECOMMENDER"
    KNOWLEDGE_RETRIEVER = "KNOWLEDGE_RETRIEVER"
    KNOWLEDGE_GRAPH = "KNOWLEDGE_GRAPH"

    # AI Agents & Automation
    AI_AGENT = "AI_AGENT"
    AI_ORCHESTRATOR = "AI_ORCHESTRATOR"
    AUTONOMOUS_DECISION_AGENT = "AUTONOMOUS_DECISION_AGENT"
    CONVERSATIONAL_AGENT = "CONVERSATIONAL_AGENT"
    RPA_AGENT = "RPA_AGENT"
    MULTI_AGENT_SYSTEM = "MULTI_AGENT_SYSTEM"
    COOPERATIVE_AI_AGENT = "COOPERATIVE_AI_AGENT"
    ACTION_PLANNER = "ACTION_PLANNER"
    REASONING_AGENT = "REASONING_AGENT"
    GOAL_ORIENTED_AGENT = "GOAL_ORIENTED_AGENT"
    TASK_AUTOMATION_AGENT = "TASK_AUTOMATION_AGENT"
    AGENTIC_WORKFLOW_MANAGER = "AGENTIC_WORKFLOW_MANAGER"

    # Text Processing
    TEXT_GENERATOR = "TEXT_GENERATOR"
    SENTIMENT_ANALYZER = "SENTIMENT_ANALYZER"
    ENTITY_RECOGNIZER = "ENTITY_RECOGNIZER"
    TOPIC_MODELING = "TOPIC_MODELING"
    TEXT_NORMALIZER = "TEXT_NORMALIZER"
    TEXT_EMBEDDING_GENERATOR = "TEXT_EMBEDDING_GENERATOR"
    PLAGIARISM_DETECTOR = "PLAGIARISM_DETECTOR"
    TEXT_CLUSTERER = "TEXT_CLUSTERER"
    GRAMMAR_CHECKER = "GRAMMAR_CHECKER"
    TEXT_TO_SPEECH = "TEXT_TO_SPEECH"
    SPEECH_TO_TEXT = "SPEECH_TO_TEXT"

    # Audio Processing
    SPEECH_RECOGNIZER = "SPEECH_RECOGNIZER"
    SPEECH_SYNTHESIZER = "SPEECH_SYNTHESIZER"
    AUDIO_NOISE_FILTER = "AUDIO_NOISE_FILTER"
    MUSIC_RECOMMENDER = "MUSIC_RECOMMENDER"
    AUDIO_FINGERPRINTING = "AUDIO_FINGERPRINTING"
    SPEAKER_VERIFICATION = "SPEAKER_VERIFICATION"

    # Image Processing
    IMAGE_GENERATOR = "IMAGE_GENERATOR"
    IMAGE_CLASSIFIER = "IMAGE_CLASSIFIER"
    OBJECT_DETECTOR = "OBJECT_DETECTOR"
    FACIAL_RECOGNIZER = "FACIAL_RECOGNIZER"
    IMAGE_SEGMENTATION = "IMAGE_SEGMENTATION"
    QR_CODE_SCANNER = "QR_CODE_SCANNER"
    OPTICAL_CHARACTER_RECOGNITION = "OPTICAL_CHARACTER_RECOGNITION"
    IMAGE_ENHANCER = "IMAGE_ENHANCER"
    IMAGE_CAPTIONING = "IMAGE_CAPTIONING"
    DEEPFAKE_DETECTOR = "DEEPFAKE_DETECTOR"

    # Video Processing
    VIDEO_PROCESSOR = "VIDEO_PROCESSOR"
    ACTION_RECOGNIZER = "ACTION_RECOGNIZER"
    VIDEO_SUMMARIZER = "VIDEO_SUMMARIZER"
    SCENE_DETECTOR = "SCENE_DETECTOR"
    VIDEO_CAPTIONING = "VIDEO_CAPTIONING"
    VIDEO_ENHANCER = "VIDEO_ENHANCER"
    VIDEO_STREAM_ANALYZER = "VIDEO_STREAM_ANALYZER"

    # Data Science & AI
    TIME_SERIES_ANALYZER = "TIME_SERIES_ANALYZER"
    MODEL_TRAINER = "MODEL_TRAINER"
    MODEL_EVALUATOR = "MODEL_EVALUATOR"
    EMBEDDING_GENERATOR = "EMBEDDING_GENERATOR"
    CLUSTER_ANALYZER = "CLUSTER_ANALYZER"
    FEDERATED_TRAINER = "FEDERATED_TRAINER"
    FEDERATED_AGGREGATOR = "FEDERATED_AGGREGATOR"
    BIAS_DETECTOR = "BIAS_DETECTOR"
    FAIRNESS_AUDITOR = "FAIRNESS_AUDITOR"
    ANOMALY_DETECTOR = "ANOMALY_DETECTOR"
    OUTLIER_DETECTOR = "OUTLIER_DETECTOR"
    FEATURE_ENGINEER = "FEATURE_ENGINEER"
    HYPERPARAMETER_TUNER = "HYPERPARAMETER_TUNER"

    # Cybersecurity & Privacy
    ENCRYPTOR = "ENCRYPTOR"
    DECRYPTOR = "DECRYPTOR"
    AUTHENTICATOR = "AUTHENTICATOR"
    BIOMETRIC_VERIFIER = "BIOMETRIC_VERIFIER"
    SECURITY_SCANNER = "SECURITY_SCANNER"
    CYBER_THREAT_DETECTOR = "CYBER_THREAT_DETECTOR"
    FIREWALL_ANALYZER = "FIREWALL_ANALYZER"
    PHISHING_DETECTOR = "PHISHING_DETECTOR"
    ZERO_KNOWLEDGE_PROVER = "ZERO_KNOWLEDGE_PROVER"
    DATA_ANONYMIZER = "DATA_ANONYMIZER"

    # Blockchain & Web3
    BLOCKCHAIN_VERIFIER = "BLOCKCHAIN_VERIFIER"
    SMART_CONTRACT_AUDITOR = "SMART_CONTRACT_AUDITOR"
    NFT_METADATA_EXTRACTOR = "NFT_METADATA_EXTRACTOR"
    ONCHAIN_INDEXER = "ONCHAIN_INDEXER"
    TRANSACTION_ANALYZER = "TRANSACTION_ANALYZER"
    ZERO_KNOWLEDGE_PROOF_GENERATOR = "ZERO_KNOWLEDGE_PROOF_GENERATOR"
    DECENTRALIZED_IDENTITY_VERIFIER = "DECENTRALIZED_IDENTITY_VERIFIER"
    WEB3_DATA_INDEXER = "WEB3_DATA_INDEXER"

    # Finance & Trading
    MARKET_PREDICTOR = "MARKET_PREDICTOR"
    TRADING_SIGNAL_GENERATOR = "TRADING_SIGNAL_GENERATOR"
    RISK_ANALYZER = "RISK_ANALYZER"
    PORTFOLIO_OPTIMIZER = "PORTFOLIO_OPTIMIZER"
    FRAUD_DETECTOR = "FRAUD_DETECTOR"
    FINANCIAL_REPORT_SUMMARIZER = "FINANCIAL_REPORT_SUMMARIZER"
    CREDIT_SCORE_EVALUATOR = "CREDIT_SCORE_EVALUATOR"
    LOAN_ELIGIBILITY_ASSESSOR = "LOAN_ELIGIBILITY_ASSESSOR"

    # Healthcare & Medical AI
    MEDICAL_IMAGE_ANALYZER = "MEDICAL_IMAGE_ANALYZER"
    DISEASE_PREDICTOR = "DISEASE_PREDICTOR"
    GENOME_SEQUENCE_ANALYZER = "GENOME_SEQUENCE_ANALYZER"
    HEALTH_RISK_EVALUATOR = "HEALTH_RISK_EVALUATOR"
    MEDICATION_RECOMMENDER = "MEDICATION_RECOMMENDER"
    EHR_PROCESSOR = "EHR_PROCESSOR"

    # Robotics & IoT
    ROBOTICS_CONTROLLER = "ROBOTICS_CONTROLLER"
    SENSOR_DATA_ANALYZER = "SENSOR_DATA_ANALYZER"
    SMART_HOME_ASSISTANT = "SMART_HOME_ASSISTANT"
    AUTONOMOUS_NAVIGATION = "AUTONOMOUS_NAVIGATION"
    INDUSTRIAL_IOT_MONITOR = "INDUSTRIAL_IOT_MONITOR"

    # Code & Development
    CODE_GENERATOR = "CODE_GENERATOR"
    CODE_ANALYZER = "CODE_ANALYZER"
    BUG_DETECTOR = "BUG_DETECTOR"
    LOG_ANALYZER = "LOG_ANALYZER"
    SQL_QUERY_OPTIMIZER = "SQL_QUERY_OPTIMIZER"
    API_AUTOMATION_AGENT = "API_AUTOMATION_AGENT"

    # Miscellaneous
    MULTIMODAL_FUSION = "MULTIMODAL_FUSION"
    DATA_COMPRESSION_ENGINE = "DATA_COMPRESSION_ENGINE"
    OTHER = "OTHER"  # Allow for unspecified or custom capabilities

    def __str__(self) -> str:
        return self.value  # Ensures enum values behave as strings
