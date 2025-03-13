# Roadmap for Cross-Platform Excel API App

This document outlines the end-to-end plan and technology stack for building an application that:
- Reads an Excel file containing tracking numbers.
- Calls the Posta API ([API Spec](https://www.postaonline.cz/dokumentaceapi/b2b/redoc/B2B3-ZSKService/B2B-ZSKService-1.9.0.yaml#operation/getParcelStatusCurrent)) to retrieve each consignment’s current status.
- Writes the result back to the Excel file, inserting the status next to the corresponding tracking number.
- Runs as a standalone executable on both macOS and Windows.

## 1. Overview & Goals

- **Input:** Excel file with tracking numbers.
- **Process:** For each tracking number, invoke the API to fetch the latest consignment status.
- **Output:** Update the same Excel file (or generate a new one) with an additional column containing the retrieved status.
- **Platform:** Cross-platform support (macOS & Windows).

## 2. Technology Stack

### Programming Language & Frameworks
- **Language:** Python 3.10+  
  *Python is mature, has excellent libraries for HTTP requests, Excel file manipulation, and offers simple cross-platform packaging options.*
  
- **Excel Handling:** 
  - **pandas** (for data manipulation) and/or **openpyxl** (for direct Excel file I/O).
  
- **HTTP/API Requests:**
  - **requests** library for interacting with the Posta API.
  
- **CLI/GUI:**
  - **CLI:** Use Python’s built-in `argparse` (or **click** for enhanced CLI UX).
  - **Optional GUI:** Consider **Tkinter** (bundled with Python) or **PyQt5/PySide2** for a modern interface if needed.

### Build & Packaging
- **Executable Packaging:** 
  - **PyInstaller** to bundle your app into standalone executables for both macOS and Windows.
  
- **Virtual Environment & Dependency Management:**
  - **venv** or **virtualenv** for environment isolation.
  - **pip** (or **poetry**/ **pipenv** for advanced dependency management).

### Testing & CI/CD
- **Testing Framework:** 
  - **pytest** for unit and integration tests.
- **Continuous Integration:**
  - **GitHub Actions** to automate testing and build pipelines across multiple platforms.

### Additional Tools & Best Practices
- **Version Control:** Git (hosted on GitHub, GitLab, etc.)
- **Documentation:** Markdown files (like this roadmap) and inline code documentation.
- **Linting/Formatting:** flake8, black (for code style consistency).

## 3. Application Architecture

### Modular Design
1. **Excel I/O Module:**  
   - Reads the input Excel file and writes the output with an added “Status” column.
   - Libraries: pandas/openpyxl.

2. **API Client Module:**  
   - Handles HTTP calls to the Posta API.
   - Manages error handling, retries, and logging.
   - Libraries: requests.

3. **Processing & Orchestration Module:**  
   - Iterates over tracking numbers, calls the API, processes responses, and integrates results with the Excel module.
   - Ensures data integrity and logging of successes/failures.

4. **User Interface Module:**  
   - **CLI:** Command-line arguments for input file, output file, verbosity, etc.
   - **Optional GUI:** Simple desktop interface for file selection and process feedback.

5. **Packaging & Deployment:**  
   - Scripts for building executables using PyInstaller.
   - CI/CD scripts (GitHub Actions) for automated builds and testing.

## 4. Milestones & Timeline

### Phase 1: Project Setup & Environment
- [ ] Set up Git repository.
- [ ] Create virtual environment and define dependency list.
- [ ] Define project structure and initial README.

### Phase 2: Core Functionality Development
- [ ] **Module 1:** Develop Excel I/O functions.
  - Read tracking numbers.
  - Write statuses back to Excel.
- [ ] **Module 2:** Develop API client for Posta service.
  - Implement error handling and logging.
- [ ] **Module 3:** Integrate modules into a cohesive workflow.
  - Test end-to-end processing with sample data.

### Phase 3: User Interface & Enhancements
- [ ] **CLI Interface:** 
  - Implement using argparse/click.
- [ ] **Optional GUI:**
  - Prototype a simple GUI using Tkinter or PyQt.
- [ ] Integrate progress indicators and user notifications.

### Phase 4: Testing & Quality Assurance
- [ ] Write unit tests with pytest for each module.
- [ ] Set up integration tests for the complete workflow.
- [ ] Integrate code linting and formatting checks.

### Phase 5: Packaging & Deployment
- [ ] Configure PyInstaller scripts for both macOS and Windows builds.
- [ ] Set up GitHub Actions CI/CD pipeline for automated testing and builds.
- [ ] Final manual testing on both platforms.

### Phase 6: Documentation & Release
- [ ] Finalize user documentation and roadmap.
- [ ] Release version 1.0 executable builds for end-users.
- [ ] Gather feedback and plan iterative improvements.

## 5. Future Enhancements
- **Enhanced Error Handling:** More robust retry logic and offline logging.
- **Configuration Management:** Support for custom API keys, endpoints, and settings via a config file.
- **Advanced UI:** Consider a more modern GUI framework (e.g., Electron with a Python backend via Eel or Flask) if feature requirements expand.
- **Reporting:** Additional output formats (CSV, PDF summaries) and logging dashboards.

---

This roadmap provides a state-of-the-art, maintainable, and modular approach to your project. It leverages proven libraries and modern best practices to ensure that your application is robust, testable, and easily deployable across multiple platforms.
