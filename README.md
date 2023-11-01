# On Track - Off-Road Track Generation Web Application

On Track is an exciting web application that allows you to create and explore off-road tracks for 4x4 vehicles. With the power of user-generated content On Track provides a seamless experience for off-road enthusiasts. This README will guide you through the project's components, setup, and usage.

## Features

- **Off-Road Track Generation**: Create off-road tracks based on the tracks shared by other users.

- **User-Friendly Interface**: For creating, viewing, and downloading tracks.

## Technologies Used

- **Server-Side**:
  - Language: Python.
  - Framework: Flask.  

- **Client-Side**:
- - Language: TypeScript.
  - Framework: Angular 12.
  - Major third-party:
    * Leaflet - a JavaScript library that integrated into the client-side for interactive maps.
    * Open Source Map (OSM) - OSM provides map data for a rich and customizable mapping  with routing abilities

- **Databases**:
  - Neo4J: The application utilizes a Neo4J graph database to efficiently store and query track information.
  - PostgreSQL: PostgreSQL is used for site operations, ensuring robust and reliable data management.

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/on-track.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd on-track
   ```

3. **Server-Side Setup**:
   - Ensure you have Python installed. You can install it from [Python's official website](https://www.python.org/downloads/).

   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

4. **Client-Side Setup**:
   - Navigate to the `client` directory:
     ```bash
     cd client
     ```

   - Install Angular CLI globally (if not already installed):
     ```bash
     npm install -g @angular/cli
     ```

   - Install client-side dependencies:
     ```bash
     npm install
     ```

5. **Database Setup**:
   - Install and set up Neo4J and PostgreSQL databases as required for your environment.

6. **Configuration**:
   - Create a configuration file, e.g., `config.py`, for server-side configuration, including database connection details and any other application-specific settings.

7. **Run the Application**:
   - Start the server-side application:
     ```bash
     python app.py
     ```

   - Start the client-side application:
     ```bash
     ng serve
     ```

   Access the application at `http://localhost:4200` by default.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

We would like to express our gratitude to the open-source community, which has provided invaluable tools and resources that made this project possible.

---

Get ready for some off-road adventure with On Track! Explore new places, challenge yourself with different off-road scenarios, and share your tracks with fellow enthusiasts. For more information and updates, visit my [GitHub repository](https://github.com/eyalcohencs/on-track).

Happy off-roading! 🌄🚙💨
