<div align="center">
<h3 align="center">Web Optimized Smart Resource Allocation</h3>
<p align="center">
My diploma thesis focused on analysis and development of optimization and smart resource allocation systems using web programming.
<br/>
<br/>
<a href="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation"><strong>Explore the docs</strong></a>
</p>
</div>

 ### Built With

This project was built with the following:
- <a href="https://www.python.org/">Python</a> for the optimization algorithm.
- <a href="https://pandas.pydata.org/">Pandas</a>, a Python library, for data manipulation.
- <a href="https://openpyxl.readthedocs.io/en/stable/">Openpyxl</a>, a Python library, for writing performance charts to the results Excel files.
- <a href="https://developers.google.com/optimization/">Google OR-Tools</a> for modeling and solving optimization problems.
- <a href="https://www.djangoproject.com/">Django</a> for the web integration.
- <a href="https://www.w3schools.com/html/">HTML</a>.
- <a href="https://www.w3schools.com/css/">CSS</a>. 
- <a href="https://www.w3schools.com/js/">JavaScript</a>. 
- <a href="https://code.visualstudio.com/">VS Code</a> for the IDE.


 ## About The Project
 
<p align="center">
<img src="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation/blob/main/screenshots/home.png"  title="home"/>
</p>

Web Optimized Smart Resource Allocation is a web-based optimization system that solves complex optimization and resource allocation problems using Constraint Programming techniques. It is scalable and capable of solving various optimization problems with high efficiency and speed, simply by configuring its algorithm to suit each problem's specific needs. To demonstrate its capabilities, the system is currently being applied to a real student allocation problem for the <a href="https://www.ict.ihu.gr/en/">department</a> I study in, showcasing both its practical relevance and performance.

## Getting Started
 
 ### Installation
 
<p>Please follow the following steps for successful installation:</p>

1. **Clone the repo**.
   ```sh
   git clone https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation
   ```
2. **Install a <a href="https://www.python.org/downloads/">Python version</a> from its official website**.
3. **Install <a href="https://aka.ms/vs/17/release/vc_redist.x64.exe">Visual C++ Redistributable for Visual Studio 2015-2022</a> for Google OR-Tools to work, if not having already**.
  
## How To Run

For a successful run, follow these steps:

1. **Navigate to the path where the repo is cloned and enter "cmd" instead of its directory path in Windows Explorer**.

2. **With the terminal open, navigate to the project's path**.
    ```sh
   cd web_allocation_project
    ```
3. **Activate and enter the virtual environment with all the required libraries installed**.
    ```sh
   .\venv\Scripts\activate
    ```
4. **Start the development server**.
    ```sh
   python manage.py runserver
    ```

 ## Features
### Users can

- View information about the development process on the home page.
- Select the semester for which students should be allocated to available courses.
- Upload Excel files containing students, courses, and student preferences data.
- Clear previously uploaded files.
- View the students' table who need to be allocated.
- Run the optimization algorithm by specifying minimum and maximum course size limits in the allocation page.
- Clear the course size limits.
- View the allocation results, including student assignments per course and detailed information, such as performance metrics.
- Re-run the allocation process with the same data using different course limits.
- Download the results as an Excel file.
- Compare results from different allocations using custom naming in the results Excel files. 
- View charts demonstrating the performance of the optimization algorithm.

### Security & more:
- Responsive web design.
- Data preprocessing from multiple Excel sheets, including handling of NaN values and filtering only the students with course preferences.
- Cross Site Request Forgery (CSRF) protection.
- **Validation** for: 
  - File type and structure of uploaded Excel files.
  - Semester selection. 
  - Course limit inputs for allocation.

 ## Usage

Here are some screenshots of the system running showing the features mentioned:
<table>
  <tr>
    <td>
     Home page
      <img src="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation/blob/main/screenshots/home.png" title="home"/>
    </td>
    <td>
     Home page - Submitting data
      <img src="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation/blob/main/screenshots/home submit data.png"  title="home_submit_data"/>
    </td>
  </tr>
  <tr>
    <td>
     Allocation page
      <img src="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation/blob/main/screenshots/allocation.png"  title="allocation"/>
    </td>
    <td>
     Allocation page - Submitting minimum and maximum course limits
      <img src="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation/blob/main/screenshots/allocation submit min-max.png"  title="allocation_submit_min-max"/>
    </td>
    <td>
     Allocation page - Download allocation results
      <img src="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation/blob/main/screenshots/download allocation results.png"  title="download_allocation_results"/>
    </td>
</tr>
</table>

<p align="center">
 Responsive design 
</br>
 <img src="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation/blob/main/screenshots/responsive.gif" title="responsive"/>
</p>

### Allocation Results

The allocation results help professors understand how effectively students were assigned to their preferred courses, and whether that led to high satisfaction. They also highlight the most preferred courses and how different course limits affect overall satisfaction. To present these insights, the allocation page includes the following tables:
- **Students for Allocation**: Basic student information along with their ranked course preferences.
- **Allocated Students**: Lists students allocated to each course, including preference satisfaction and other relevant student data.
- **Allocated Students with < 100% preference satisfaction**: Shows students whose top 6 preferences were not fully met, along with their satisfaction ratio and the preferences they did receive.
- **Number of Allocated Students per Course**: Displays how many students were allocated to each course.


### Performance Statistics:

The following performance metrics demonstrate the effectiveness of the developed optimization algorithm, achieving high average top 6 preferences satisfaction rates of up to 99.72%, as well as excellent 1st preference satisfaction ratios, especially for the most in-demand courses.
<table>
  <tr>
    <td>
     Average student top 6 preferences ratio (7 and 35 course limits)
      <img src="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation/blob/main/screenshots/average student top 6 preferences ratio.png"  title="average_student_top_6_preferences_ratio"/>
    </td>
    <td>
     1st preference satisfaction ratio
      <img src="https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation/blob/main/screenshots/1st preference satisfaction ratio.png"  title="1st_preference_satisfaction_ratio"/>
    </td>
 </tr>
 </table>


For a closer look, click on the images and open them from the **screenshots** folder.
 
## Collaborators

<p>This project was developed for my diploma thesis acquiring the Master's degree in the Department of Computer, Informatics and Telecommunications Engineering at International Hellenic University.</p>
<table>
<tr>

<td align="center">
<a href="https://github.com/helenzina">
<img src="https://avatars.githubusercontent.com/u/128386591?v=4" width="100;" alt="Helen Zina"/><br>
<sub>
<b>Helen Zina (Me)</b>
</sub>
</a>
</td>

</tr>
</table>

 ## License

Distributed under the MIT License. See the LICENSE file for more information.

 ## Contact
 
If you have any questions or suggestions, feel free to reach out to me:
- Helen Zina - helen.zina@yahoo.com
- Project Link: https://github.com/helenzina/Web-Optimized-Smart-Resource-Allocation


 ## Acknowledgments

The resources that helped me through this whole process were some of the following:

- [Google OR-Tools for Constraint Programming](https://www.youtube.com/watch?v=hod0L0zfnZs)
- [A practical introduction to Constraint Programming using CP-SAT and Python - pganalyze](https://pganalyze.com/blog/a-practical-introduction-to-constraint-programming-using-cp-sat)
- [How to Use Django Sessions](https://www.youtube.com/watch?v=N-R5mT-nIDk)
- [Serialize and Deserialize complex JSON in Python - GeeksForGeeks](https://www.geeksforgeeks.org/python/serialize-and-deserialize-complex-json-in-python/)
- [Submit Form Without Page Reload | Ajax | Ajaxify Django](https://www.youtube.com/watch?v=dccWcCpZI9w/)
  
A special thank you to the <a href="https://discord.com/invite/ENkQrdf">Google OR-Tools Discord server community</a> for your undeniable help making me understand the fundamentals of Constraint Programming using the following guide:
- [The CP-SAT Primer: Using and Understanding Google OR-Tools' CP-SAT Solver](https://d-krupke.github.io/cpsat-primer/)


