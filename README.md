# BalikovnaTracker - Czech Post Package Status Tracker

A Python-based utility that automates tracking of multiple Czech Post (Česká pošta) packages by processing Excel files containing tracking numbers.

## 🚀 Features

- Bulk tracking number processing from Excel files
- Direct integration with Czech Post's official API
- Automatic status updates written back to Excel
- Cross-platform support (Windows & macOS)
- Simple command-line interface

## 📋 Requirements

- Python 3.10+
- Excel file with tracking numbers
- Czech Post API credentials

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/vojtechryp/BalikovnaTracker-CPostExternalTrack-Trace.git
cd BalikovnaTracker-CPostExternalTrack-Trace
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Prepare your Excel file with tracking numbers
2. Run the tracker:
```bash
python src/main.py --input tracking_numbers.xlsx --output results.xlsx
```

## 📊 Excel File Format

### Input Format
Your Excel file should contain:
- A column with tracking numbers
- Headers in the first row

### Output Format
The program will:
- Keep all original data
- Add a new column with current package statuses
- Add timestamp of last check

## ⚙️ Configuration

Create a `.env` file in the project root:
```
CPOST_API_KEY=your_api_key_here
CPOST_API_SECRET=your_api_secret_here
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Czech Post API Documentation](https://www.postaonline.cz/dokumentaceapi)
- [Project Roadmap](roadmap.md)

## ⚠️ Disclaimer

This is an unofficial tool and is not affiliated with Česká pošta.
