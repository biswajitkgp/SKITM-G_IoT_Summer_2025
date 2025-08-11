# IoT Internship at SKITM&G, Jaipur

Welcome to the resource repository for the IoT Product Design Workshop held at the **Center of Excellence in IoT, SKITM&G, Jaipur**. This repository contains all the necessary files, code, and guides to build the IoT project from scratch.



## 📋 The Project Workflow

This repository is organized to follow the exact path we took during the project. Each numbered folder marks a key stage in our journey from an idea to a finished product.

1.  [Phase 1: Introduction to Hardware for IoT](#-phase-1-introduction-to-hardware-for-iot)
2.  [Phase 2: Simulation & Code Prototyping (Wokwi)](#-phase-2-simulation--code-prototyping-wokwi)
3.  [Phase 3: Setting Up Your ESP32 Board](#-phase-3-setting-up-your-esp32-board)
4.  [Phase 4: Designing a Custom PCB (EasyEDA)](#-phase-4-designing-a-custom-pcb-easyeda)
5.  [Phase 5: The Final Project Code](#-phase-5-the-final-project-code)

---

### 🚀 Phase 1: Introduction to Hardware for IoT

We started with a presentation covering the fundamentals of designing hardware for the Internet of Things. This session provided the core concepts for our entire project.

* **Find the full presentation in:** `1_Presentation_Hardware_For_IoT/`

### 🔌 Phase 2: Simulation & Code Prototyping (Wokwi)

Before building the physical circuit, we used the Wokwi online simulator to design and test everything. This is where we wrote our first version of the MicroPython code and made sure our schematic worked as expected.

* **Find all simulation files in:** `2_Simulation_Wokwi/`
* **Or view the live project on Wokwi:** `[Link to your public Wokwi project]`

### 💻 Phase 3: Setting Up Your ESP32 Board

This was our first hands-on step. We prepared our ESP32 development boards by flashing them with the MicroPython firmware, making them ready for our own code.

**A detailed guide for this process is located in `3_ESP32_Setup_and_Firmware/Flashing_Guide.md`**.

The guide covers:
1.  How to check which USB-to-Serial chip your board has (CP2102 vs. CH340).
2.  Where to download and install the correct drivers.
3.  A step-by-step walkthrough of flashing MicroPython using the Thonny IDE.

### 🛠️ Phase 4: Designing a Custom PCB (EasyEDA)

With a working prototype, we moved to EasyEDA to design a professional Printed Circuit Board (PCB) for our project. This is how we created a permanent and reliable home for our components.

All the design files are here for you to use:
* **EasyEDA project files are in:** `4_Hardware_Design_EasyEDA/project_files/`
* **Gerber files (for manufacturing) are in:** `4_Hardware_Design_EasyEDA/gerbers/`

### ✅ Phase 5: The Final Project Code

This is the final version of the MicroPython code, written specifically to run on the custom PCB we designed.

* **Find the final source code in:** `5_Final_Project_Code/`

---

## 📚 Essential Resources

* **Component Datasheets:** Key datasheets are located in `6_Resources/datasheets/`.
* **Useful Links:** A list of online calculators, component suppliers, and other helpful sites is available in `6_Resources/useful_links.md`.

## 🙏 Acknowledgements

A special thank you to **SKITM&G, Jaipur**, for an excellent internship program and the opportunity to work on this project.

---

## 📄 License

This project is open-source and licensed under the **MIT License**. See the `LICENSE` file for more details.
