<h1>Nautilus - An efficient and dynamic ship routing algorithm prototype developed as a part of SIH 2024.</h1>

Problem Statement ID	- 1658<br>
Problem Statement Title	- Development of a versatile and fast algorithm for the optimal ship routing<br>
Link: https://www.sih.gov.in/sih2024PS (In search, type in the Problem Statement ID as 1658)<br>

Organization - Ministry of Earth Sciences<br>
Department - Indian National Center for Ocean Information Services (INCOIS)<br>
Category - Software<br>
Theme	- Transportation & Logistics<br>

Description -<br>
Background: <br>
Most of the goods are transported around the world by shipping which relies heavily on fossil fuels for powering. Given the expenditure of the shipping industry on the fuel, a main objective of a shipping company is to optimize the ship route for the least fuel consumption. Depending on the type and purpose of the voyage, it is also desirable to optimize several other parameters such as, the travel time, passenger comfort and route safety, to avoid any damage to the ship, cargo, crew and passengers. Optimization of each of these parameters serves a purpose. For instance, an energy efficient route may not be safe in terms of weather. Therefore, to avoid loss of life and property, route weather safety needs to be considered. An application suggesting the optimal route based on the chosen set of optimal parameters for any voyage between two ports in the Indian Ocean, will immensely benefit the Indian shipping industry. Description: At the heart of any optimal ship routing application lies the optimization algorithm. Although scientific literature is available on various methods of optimizing the ship routes, given the commercial potential, there are no applications available publicly which can be customized for the Indian Ocean region. The optimization methods reported in literature range in complexity, computation time, versatility, etc. Various factors, such as, the forcings (surface winds, currents and waves), design of the ship and ship drift characteristics, impact the ship├ö├ç├ûs motion at sea. The optimal route must be continually evolving because the weather conditions keep changing as a ship proceeds on its voyage. Therefore, it is crucial to choose a suitable optimization method that can optimize several parameters for a range of ships (with varying type, dimensions, drift characteristics of a ship) and develop an algorithm to return an optimal route within a reasonable computational time. The algorithm can optimize for the voyage time and safety to begin with but with a scope for addition of more optimization parameters. To get an idea of the problem, please visit: https://www.youtube.com/watch?v=ct9v-mQgYqE ii) https://www.youtube.com/watch?v=wCTdHRTWtNI<br>

Expected Solution: Identification of a versatile optimization method and development of a reasonably fast algorithm, preferably written in an open-source programming language such as Python<br>

<h2>Working proof of the application:</h2>
<br>
<img src="https://github.com/user-attachments/assets/55b300a4-8f5e-4138-a9f5-3270dbd021cb" width=75% height=75%>
<br>
<br>


Simple user interface for testing and choosing source and destination ports:
<br>
<img src="https://github.com/user-attachments/assets/5fa3eb5d-970c-49a2-b3cd-711acaaf16d1" width=75% height=75%>
<br>
<br>


Information of different weather factors at every point:
<br>
<img src="https://github.com/user-attachments/assets/1c6c1bb8-8fe4-4a6e-a796-42a465c154f3" width=75% height=75%>
<br>
<br>


Proof of long distance travels:
<br>
<img src="https://github.com/user-attachments/assets/5f19439d-3187-44c7-8c2b-3fc5e3ab1a88" width=75% height=75%>
<br>
<br>


<b>How to run the application:</b><br><br>

Step 1: Download the project as zip file and extract its contents.<br><br><br>
Step 2: Make the following changes-<br>

        In file pathfinding.py, change the following path locations on lines mentioned below to your respective system path locations of the files:
          line 22: df = load_csv_safe(r"C:\Users\abhir\OneDrive\Desktop\Nautilus\ocean_points.csv")
          line 27: ports_df = load_csv_safe(r"C:\Users\abhir\OneDrive\Desktop\Nautilus\ports_coordinates.csv")
          line 102: df = load_csv_safe(r"C:\Users\abhir\OneDrive\Desktop\Nautilus\updated_coordinates.csv")

        In file dataGenerator.py, change the following path locations on lines mentioned below to your respective system path locations of the files:
          line 18: input_csv = r"C:\Users\abhir\OneDrive\Desktop\Nautilus\ocean_points.csv"
          line 56: save_to_csv(df_updated, r"C:\Users\abhir\OneDrive\Desktop\Nautilus\updated_coordinates.csv")

        In file app.py, change the following path location on line mentioned below to your respective system path location of the file:
          line 50: script_path = 'C:\\Users\\abhir\\OneDrive\\Desktop\\Nautilus\\pathfinding.py'
<br>Step 3: Run two files simultaneously on your system on two terminals as shown below and navigate to the following URL: http://127.0.0.1:5000/
<br>
<img src="https://github.com/user-attachments/assets/df1af75c-dfa7-4d1e-9590-9c9537b12e6f" width=75% height=75%>
<br>
<br>
