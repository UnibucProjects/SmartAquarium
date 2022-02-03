<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/UnibucProjects/SmartAquarium">
    <img src="https://smartbrandaquariums.files.wordpress.com/2020/01/cropped-logo-smart-brands.png" alt="Logo" width="200">
  </a>

  <h3 align="center">Smart Aquarium</h3>

  <p align="center">
    The application is a mock IoT device, simulating a Smart Aquarium 
    <br />
    <a href="https://docs.google.com/document/d/10eDxDCgwnqeRekGz2bW9aIY8jzL7HC1c0HLMZZPzC9k/edit?usp=sharing"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/UnibucProjects/SmartAquarium/issues">Report Bug</a>
    ·
    <a href="https://github.com/UnibucProjects/SmartAquarium/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The purpose of this smart aquarium is to facilitate and automate the care of fish, coming to the aid of both farms and pet shops, as well as that of fish owners. It will take data from the environment with the help of sensors (light, temperature, motion, etc.) and will take into account the user's preferences, to provide easy care, tailored to the needs of each type of ecosystem.

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [SQLite](https://www.sqlite.org/index.html)
* [Mosquitto](https://mosquitto.org/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* <a href="https://realpython.com/installing-python/">Install Python3</a>
* Mosquitto (For this app, we will use the default configurations of mosquitto)<br/><br/>
  MacOS<br/>
  ```sh
  brew install mosquitto
  ```
  Windows: <a href="https://mosquitto.org/download/">Download mosquitto</a>

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/UnibucProjects/SmartAquarium.git
   ```
2. Install venv if not already installed:
   ```sh
   pip install virtualenv
   ```
3. Create an environment:<br/><br/>
   MacOS
   ```sh
   python3 -m venv ./
   ```
   Windows
   ```sh
   python -m venv venv
   ```
4. Activate environment:<br/><br/>
   MacOS/Linux
   ```sh
   source venv/bin/activate
   ```
   Windows
   ```sh
   .venv\Scripts\activate.bat
   ```
5. Install libraries
   ```sh
   pip install -r requirements.txt
   ```
6. Set environment value for development:<br/><br/>
   MacOS
   ```sh
   export FLASK_ENV=development
   ```
   CMD
   ```sh
   set FLASK_ENV=development
   ```
   PowerShell
   ```sh
   $env:FLASK_ENV = "development"
   ```
7. Initialize (or reinitialize) database:
   ```sh
   flask init-db
   ```  
8. Open `flaskr` folder and add some data in the database(this step should be repeated after every `flask init-db` command)
    ```sh
    cd flaskr
    python initialize_database.py
    ```
10. Run
    ```sh
    flask run
    ```  
   
### RESTler installation

1. <a href="https://docs.microsoft.com/en-us/dotnet/core/install/windows?tabs=net60">Install .NET 5.0</a>
2. Download RESTler repository in the same folder where the project is and open the RESTler folder
    ```sh
    git clone https://github.com/microsoft/restler-fuzzer.git
    cd restler-fuzzer
    ```
3. Create a folder for RESTler binary files
    ```sh
    mkdir ../restler_bin
    ```
4. Build RESTler project
    ```sh
    python ./build-restler.py --dest_dir ../restler_bin --dotnet_package_source https://api.nuget.org/v3/index.json
    ```
5. Compile RESTler project
    ```sh
    cd ../restler_bin
    dotnet ./restler/Restler.dll compile --api_spec ../SmartAquarium/openapi.json
    ```
6. Run RESTler project
    ```sh
    cd Compile
    dotnet ../restler/Restler.dll test --grammar_file grammar.py --dictionary_file dict.json --settings engine_settings.json --no_ssl
    ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

To try out the application firstly run `python app.py` in the flaskr directory of the project.<br/>
Then, to listen to messages on the `python/mqtt` topic run `mosquitto_sub -h localhost -p 1883 -t python/mqtt` (MacOS) or `.\mosquitto_sub -h localhost -p 1883 -t python/mqtt` (Windows) in the mosquitto folder.<br/>
To start the application send a get request to `http://[::1]:5000`.

_For more examples, please refer to the [OpenAPI documentation](https://github.com/UnibucProjects/SmartAquarium/blob/main/openapi.json) and [AsyncAPI documentation](https://github.com/UnibucProjects/SmartAquarium/blob/main/asyncapi.yaml)_

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] CRUD aquariums
- [x] CRUD fish
- [x] CRUD feeding schedules
- [x] CRUD water settings
- [x] CRUD light settings
- [x] Water
    - [x] Measure temperature
    - [x] Adjust conditions
    - [x] Quality analysis
- [x] Food
    - [x] Release food
    - [x] Notify empty containers
- [x] Light
- [ ] Health
- [x] Customization

See the [open issues](https://github.com/UnibucProjects/SmartAquarium/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See <a href="https://github.com/UnibucProjects/SmartAquarium/blob/main/LICENSE">`LICENSE`</a> for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [Flask Tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/)
* [Pytest Unit Test Tutorial](https://codethechange.stanford.edu/guides/guide_flask_unit_testing.html)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/UnibucProjects/SmartAquarium.svg?style=for-the-badge
[contributors-url]: https://github.com/UnibucProjects/SmartAquarium/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/UnibucProjects/SmartAquarium.svg?style=for-the-badge
[forks-url]: https://github.com/UnibucProjects/SmartAquarium/network/members
[stars-shield]: https://img.shields.io/github/stars/UnibucProjects/SmartAquarium.svg?style=for-the-badge
[stars-url]: https://github.com/UnibucProjects/SmartAquarium/stargazers
[issues-shield]: https://img.shields.io/github/issues/UnibucProjects/SmartAquarium.svg?style=for-the-badge
[issues-url]: https://github.com/UnibucProjects/SmartAquarium/issues
[license-shield]: https://img.shields.io/github/license/UnibucProjects/SmartAquarium.svg?style=for-the-badge
[license-url]: https://github.com/UnibucProjects/SmartAquarium/blob/main/LICENSE

