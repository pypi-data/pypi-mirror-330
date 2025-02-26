# CoTKG-IDS: Chain of Thought Knowledge Graph Intrusion Detection System

## Overview
CoTKG-IDS is an advanced network intrusion detection system that combines Chain of Thought (CoT) reasoning with knowledge graphs and GraphSAGE for enhanced detection capabilities and interpretability. The system is designed to detect and classify various types of network intrusions by leveraging graph-based deep learning and knowledge representation.

## Key Features
- 🧠 Chain of Thought (CoT) enhanced reasoning for interpretable detection
- 🕸️ Dynamic knowledge graph construction from network flow data
- 📊 GraphSAGE-based network analysis for pattern detection
- 🔍 Advanced feature engineering with automated selection
- ⚖️ Intelligent data balancing for handling imbalanced attack classes
- 🎯 Multi-class attack detection with high accuracy
- 📈 Comprehensive visualization tools for analysis
- 🔄 Real-time processing capabilities
- 🛠️ Modular architecture for easy extension
- 🤖 Support for multiple LLM providers (Ollama, Qianwen)

## Architecture
```
Input Data → Feature Engineering → Knowledge Graph Construction → GraphSAGE Model → Attack Detection
    ↓               ↓                       ↓                         ↓                ↓
Preprocessing → Feature Selection → Graph Embeddings → Chain of Thought → Interpretability
```

## Installation

### Prerequisites
- Python 3.7+
- Neo4j Database 4.4+
- PyTorch 1.9+
- CUDA (optional, for GPU support)
- 8GB+ RAM recommended
- 50GB+ disk space for full dataset
- Ollama (for local LLM support)
- Qianwen API key (optional)

### Environment Setup
1. Clone the repository:
```bash
git clone https://github.com/chenxingqiang/cotkg-ids.git
cd cotkg-ids
```

2. Create and activate virtual environment:
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Or using conda
conda create -n cotkg-ids python=3.9
conda activate cotkg-ids
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### LLM Setup
You can use either Ollama (local) or Qianwen (cloud) as your LLM provider.

#### Ollama Setup

##### macOS Installation
1. Install using Homebrew:
```bash
brew install ollama
```

2. Start Ollama service:
```bash
# Start the service
brew services start ollama

# If you encounter port conflicts, try:
brew services stop ollama
pkill ollama
brew services start ollama
```

##### Linux Installation
1. Install using curl:
```bash
curl https://ollama.ai/install.sh | sh
```

2. Start Ollama service:
```bash
# Start as a service (systemd)
sudo systemctl start ollama

# Or run directly
ollama serve

# If you encounter port conflicts:
sudo systemctl stop ollama
pkill ollama
sudo systemctl start ollama
```

##### Windows Installation
1. Download the installer from [Ollama's website](https://ollama.ai/download)
2. Run the installer
3. Start Ollama:
```bash
# Using Command Prompt as Administrator
ollama.exe serve

# If you encounter port conflicts:
# First, find the process using port 11434
netstat -ano | findstr :11434
# Kill the process using its PID
taskkill /F /PID <PID>
# Then start Ollama again
ollama.exe serve
```

##### Verify Installation
Check if Ollama is running properly:
```bash
# Check server status
curl http://localhost:11434/api/health

# Or use the Python script
python scripts/setup_ollama.py --action list
```

##### Setup Models
After installing Ollama, you need to pull the required models:

```bash
# List available models
python scripts/setup_ollama.py --action list

# Pull all default models
python scripts/setup_ollama.py --action setup

# Pull specific models
python scripts/setup_ollama.py --action pull --models llama2 codellama

# Remove models
python scripts/setup_ollama.py --action delete --models model_name
```

##### Troubleshooting Ollama
If you encounter issues:

1. Port conflicts (Error: address already in use):
```bash
# macOS/Linux
sudo lsof -i :11434
pkill ollama
brew services restart ollama  # macOS
sudo systemctl restart ollama  # Linux

# Windows
netstat -ano | findstr :11434
taskkill /F /PID <PID>
```

2. Connection issues:
```bash
# Check if server is running
curl http://localhost:11434/api/health

# Check logs
# macOS
brew services info ollama
# Linux
journalctl -u ollama
# Windows
# Check Windows Event Viewer
```

3. Memory issues:
- Ensure you have at least 8GB RAM available
- Close other memory-intensive applications
- For Windows, increase page file size
- For Linux, adjust swap space

4. Model download issues:
```bash
# Try with debug logging
python scripts/setup_ollama.py --action pull --models llama2 --debug

# Check network connectivity
curl -v http://localhost:11434
```

#### Qianwen Setup
1. Get your API key from [Qianwen](https://qianwen.aliyun.com)
2. Set your API key as an environment variable:
```bash
export QIANWEN_API_KEY='your-api-key'
```

### Configure LLM Provider
Update `config/config.py` to choose your LLM provider:

```python
COT_CONFIG = {
    'provider': 'ollama',  # or 'qianwen'
    'model': 'llama2',     # for ollama
    'ollama': {
        'base_url': 'http://localhost:11434',
        'timeout': 30,
        'models': ['llama2', 'mistral', 'codellama', 'vicuna']
    },
    'qianwen': {
        'model': 'qwen-max',
        'max_tokens': 1500,
        'temperature': 0.85
    }
}
```

### Neo4j Setup
1. Install Neo4j:
```bash
# Using Docker (recommended)
docker run \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    -d neo4j:4.4

# Or download from neo4j.com
```

2. Configure Neo4j:
- Open http://localhost:7474
- Login with default credentials (neo4j/neo4j)
- Change password when prompted
- Update config/config.py with your credentials

### Data Preparation
1. Download the dataset:
```bash
python download_data.py
```

2. Verify data integrity:
```bash
python test_pipeline.py --mode data_check
```

## Usage

### Quick Start
```bash
# Run complete pipeline with default settings
python run.py

# Run only training
python run.py --mode train

# Run only testing
python run.py --mode test

# Run with test configuration
python run.py --test
```

### Python API Usage
```python
from src.main import run_full_pipeline
from config.config import DEFAULT_CONFIG

# Use default configuration
results = run_full_pipeline()

# Or customize configuration
config = DEFAULT_CONFIG.copy()
config['model']['graphsage'].update({
    'hidden_channels': 64,
    'num_layers': 3,
    'dropout': 0.2
})
results = run_full_pipeline(config=config)
```

### Configuration
The system can be configured through `config/config.py`. Key configuration sections:

```python
DEFAULT_CONFIG = {
    'model': {
        'graphsage': {
            'hidden_channels': 32,
            'num_layers': 2,
            'dropout': 0.3,
            'learning_rate': 0.01,
            'weight_decay': 0.0005
        }
    },
    'training': {
        'epochs': 20,
        'batch_size': 16,
        'early_stopping': {
            'patience': 5,
            'min_delta': 0.01
        },
        'validation_split': 0.2
    },
    'data': {
        'balancing': {
            'method': 'smote',
            'random_state': 42
        }
    },
    'neo4j': {
        'uri': 'bolt://localhost:7687',
        'username': 'neo4j',
        'password': 'password'
    },
    'cot': {
        'provider': 'ollama',
        'model': 'llama2',
        'ollama': {
            'base_url': 'http://localhost:11434',
            'timeout': 30
        }
    }
}
```

## Project Structure
```
cotkg-ids/
├── config/                 # Configuration files
├── data/                  # Data storage
│   ├── raw/              # Raw dataset
│   └── processed/        # Processed data
├── logs/                 # Log files
├── notebooks/            # Jupyter notebooks
├── results/              # Output files
│   ├── models/          # Saved models
│   └── visualizations/  # Generated plots
├── scripts/             # Utility scripts
│   └── setup_ollama.py  # Ollama setup script
├── src/                 # Source code
│   ├── data_processing/ # Data processing modules
│   ├── knowledge_graph/ # KG related code
│   ├── models/         # ML models
│   └── visualization/  # Visualization tools
└── tests/              # Test files
```

## Performance Metrics
The system is evaluated on multiple metrics:
- Detection Accuracy: ~98% on test set
- False Positive Rate: <1%
- Processing Speed: ~1000 flows/second
- Memory Usage: ~4GB for standard dataset

## Troubleshooting

### Common Issues
1. Neo4j Connection:
```bash
# Check Neo4j status
docker ps | grep neo4j
# or
service neo4j status
```

2. CUDA Issues:
```python
import torch
print(torch.cuda.is_available())  # Should return True if CUDA is properly set up
```

3. Ollama Issues:
```bash
# Check Ollama server status
curl http://localhost:11434/api/health

# List available models
python scripts/setup_ollama.py --action list

# Restart Ollama server
pkill ollama
ollama serve
```

4. Memory Issues:
- Reduce batch_size in config
- Use data sampling for large datasets
- Enable swap space if needed

### Error Messages
- "Neo4j connection failed": Check Neo4j credentials and service status
- "CUDA out of memory": Reduce batch size or model size
- "File not found": Ensure dataset is downloaded and in correct location
- "Ollama server not responding": Check if Ollama is running and accessible

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Use type hints
- Add appropriate error handling

## License
MIT License - see [LICENSE](LICENSE)

## Citation
```bibtex
@software{cotkg_ids2024,
  author = {Chen, Xingqiang},
  title = {CoTKG-IDS: Chain of Thought Knowledge Graph IDS},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/chenxingqiang/cotkg-ids}
}
```

## Contact
Chen Xingqiang  
Email: chen.xingqiang@iechor.com  
GitHub: [@chenxingqiang](https://github.com/chenxingqiang)
