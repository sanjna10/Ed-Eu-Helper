# Ed-Eu-Helper
A flask based app for education support
## Overview

Over the years E-Books, Online exams, and various other new methods have come in aiding the teaching-learning process. In the recent past, the education process has been oscillating between online and offline modes, and remains turbulent. Some aspects of the Outcome Based Education use paper based methodologies to assess student attainments. The proposed work aims to provide a simple yet effective and easy-to-use solution for the entities involved in the process to integrate all related data, enhance teaching-learning process through the plethora of analysis included in the work.

## Table of Contents

- [Tech](#tech)<br/>
- [Module](#Modules)<br/>
- [Data](#data)<br/>
- [Demo](#demo)<br/>


## Tech


**Front-End**

- [BootstrapV5](https://getbootstrap.com/)
- [HTML5](https://en.wikipedia.org/wiki/HTML5)
- [CSS3](https://www.w3schools.com/css/)
- [JS](https://www.chartjs.org/)

**Back-End**

- [Python3](https://www.python.org/download/releases/3.0/)


**Database**

- [MySQLDB](https://mysqlclient.readthedocs.io/user_guide.html)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [Pandas](https://pandas.pydata.org/docs/index.html)
- [Matplotlib](https://matplotlib.org/)

<img src="https://github.com/sanjna10/Ed-Eu-Helper/blob/main/Images/architecturefyp.drawio.png" width="80%" height="80%">

## Data

Data in this project refers to proporties involved in the visualization and attainment process. Below is the image of the flow chat that specifies how the data is transformed through different modules in the backend to generate the desired results.

<img src="https://github.com/sanjna10/Ed-Eu-Helper/blob/main/Images/data_flow.png" width="70%" height="70%">

We try to validate the importence of each question through standardised proporties used for NAAC accredition such as COs,POs, BTLs. The teaching methodologies , exam validations and mark distrution is analysed based on the above given proporties so as to change and upgrade the curriculum.


## Modules 

- Login and forgot password module : User logs in through pre-existing credentials given by the admin. Features such as forgot password is implemented so as to provide an alternate mode for logging in. This sends an OTP to the verified email account where opttions will be provided to reset the password.

- QP scanning module: Every question in an assessment has a unique property associated so as to identify its difficulty level etc. This is done through the help 3 different property metrics specified by NAAC which are COs,BTLs,DLs for the corresponding question and sub questions along with the marks allocated for each. These are followed by every college in India. This module tries to extract these features from every question given a question paper in the form of docx or pdf. This can also be extended to online quizzes and tests. A thorough QP analysis is performed with the data collected along with the student performance and attainment.

- Manual/OpenCV based mark entry process: A customized CSV file is generated given the roll numbers as rows along with the questions , marks allocated and sub question. Open CV can be used to mitigate the manual mark entry process so as to automate the system. These can be scaled to be tied up with other portals that are currently in use for quizzing and assessment etc.. These are to be stored in the db for analysis and attainment calculation.


- Analysis and reports:Analysis of CO, PO, BTL distribution of question papers along with its mark distribution is given after the compution and property extraction. Reports of student performance and marks are also given.

- Attainment and reports: Attainment calculation for each subject is done through the standard practices specified by the NAAC accredition board.

- Restricted access: Reports such as attainment can be confidential and is restricted to certian users. Hence facilities are provided to block them from further accessing certain modules.


## Demo 

**Login**
<img src="https://github.com/sanjna10/Ed-Eu-Helper/blob/main/Images/login1.PNG" width="70%" height="70%">


**Reset Password**

<img src="https://github.com/sanjna10/Ed-Eu-Helper/blob/main/Images/resetpass.PNG" width="70%" height="70%">

**Analytics and reports module**

<img src="https://github.com/sanjna10/Ed-Eu-Helper/blob/main/Images/plots.gif">

**Analysis  and update of reports onto db module**


<img src="https://github.com/sanjna10/Ed-Eu-Helper/blob/main/Images/upload.gif">

**Analysis and Attainment View**


<img src="https://github.com/sanjna10/Ed-Eu-Helper/blob/main/Images/prog.gif">







