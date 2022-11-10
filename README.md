# Data collect streamlit
App web to get clean and ordered datasets. 
- Select dataset.
- Get data and download csv.
- View sample data.
- Exploratory Data Analysis.
    - Number of columns and rows.
    - Columns data type.
    - Plot results.
    - Link to tableau public dashboard.

This app web connect to [collect API REST](https://github.com/elvestevez/collect_api) to get data.

Datasets are collected, moduled and stored by [collect load](https://github.com/elvestevez/collect_load).

### **Technology stack**
Streamlit, Python, Pandas, REST API, Tableau Public.

### **Configuration**
Get project from GitHub and create a python environment with these additional libraries:
- streamlit
- pandas
- plotly

In file web.properties you can configure the conection to microservice: heroku or local (previous download and configure [API REST project](https://github.com/elvestevez/collect_api)).

> Review requirements.txt file.

The application is deployed in streamlit cloud.

### **Usage**
You can use at url [data-collect](https://data-collect.streamlit.app/) streamlit and enjoy!

### **Folder structure**

```
└── project
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── streamlit_app.py
    ├── web.properties
    └── img
```

---

### **Next steps**
- Other technologies on cloud (Azure, AWS...).
- Improve style (css).
- Get own domain.
- Include additional download formats.
- More options to get data.
- Add new datasets (if they are availabe by API).
