medicos = [
    {
        "Nombre": "Gonzalez Juan",
        "Fecha de Nacimiento": (1995, 6, 19),
        "DNI": 48120054,
        "Especialidad": "Ortopedia y Traumatología",
        "Estado": "Disponible",
        "Paciente": {},
        "Horarios": {
            "Lunes": (9, 18),
            "Martes": (9, 18),
            "Miércoles": (9, 18),
            "Jueves": (9, 18),
            "Viernes": (9, 18),
            "Sábado": None,
            "Domingo": None
        },
        "Historial": [
            {
                "DNI": 47130033,
                "Nombre": "Kataoka Lucas",
                "Fecha de Nacimiento": (1998, 5, 23),
                "Obra Social": "Osde",
                "Fecha Turno": (2024, 5, 15)
            },
            {
                "DNI": 46120054,
                "Nombre": "Gonzalez Matias",
                "Fecha de Nacimiento": (1998, 10, 21),
                "Obra Social": "Ioma",
                "Fecha Turno": (2024, 6, 20)
            },
            {
                "DNI": 48220011,
                "Nombre": "Ramirez Sofia",
                "Fecha de Nacimiento": (1994, 9, 21),
                "Obra Social": "Galeno",
                "Fecha Turno": (2024, 7, 10)
            },
            {
                "DNI": 49340022,
                "Nombre": "Perez Martin",
                "Fecha de Nacimiento": (2000, 10, 9),
                "Obra Social": "Ioma",
                "Fecha Turno": (2024, 8, 5)
            },
            {
                "DNI": 50450033,
                "Nombre": "Lopez Valentina",
                "Fecha de Nacimiento": (1990, 1, 7),
                "Obra Social": "Osde",
                "Fecha Turno": (2024, 9, 12)
            },
            {
                "DNI": 51560044,
                "Nombre": "Torres Juan",
                "Fecha de Nacimiento": (1998, 3, 11),
                "Obra Social": "Swiss Medical",
                "Fecha Turno": (2024, 10, 3)
            },
            {
                "DNI": 95862099,
                "Nombre": "Quijada Jesus",
                "Fecha de Nacimiento": (2003, 2, 3),
                "Obra Social": "Swiss Medical",
                "Fecha Turno": (2025, 1, 8)
            },
        ],
    },
    {
        "Nombre": "Ortiz Mariana",
        "Fecha de Nacimiento": (1999, 4, 23),
        "DNI": 45063213,
        "Especialidad": "Pediatra",
        "Estado": "Disponible",
        "Paciente": {},
        "Horarios": {
            "Lunes": (9, 18),
            "Martes": (9, 18),
            "Miércoles": (9, 18),
            "Jueves": (9, 18),
            "Viernes": (9, 18),
            "Sábado": None,
            "Domingo": None
        },
        "Historial": [
            {
                "DNI": 51560044,
                "Nombre": "Torres Juan",
                "Fecha de Nacimiento": (1998, 3, 11),
                "Obra Social": "Swiss Medical",
                "Fecha Turno": (2024, 4, 12)
            },
            {
                "DNI": 52670055,
                "Nombre": "Diaz Camila",
                "Fecha de Nacimiento": (1992, 11, 21),
                "Obra Social": "Ioma",
                "Fecha Turno": (2024, 5, 18)
            },
            {
                "DNI": 53780066,
                "Nombre": "Fernandez Diego",
                "Fecha de Nacimiento": (1995, 10, 30),
                "Obra Social": "Galeno",
                "Fecha Turno": (2024, 6, 25)
            },
            {
                "DNI": 54890077,
                "Nombre": "Morales Lucia",
                "Fecha de Nacimiento": (1993, 2, 22),
                "Obra Social": "Osde",
                "Fecha Turno": (2024, 7, 30)
            },
            {
                "DNI": 55900188,
                "Nombre": "Suarez Nicolas",
                "Fecha de Nacimiento": (1999, 4, 18),
                "Obra Social": "Ioma",
                "Fecha Turno": (2024, 9, 5)
            },
        ],
    },
    {
        "Nombre": "Lopez Esteban",
        "Fecha de Nacimiento": (1988, 5, 11),
        "DNI": 43170055,
        "Especialidad": "Oculista",
        "Estado": "Disponible",
        "Paciente": {},
        "Horarios": {
            "Lunes": (9, 18),
            "Martes": (9, 18),
            "Miércoles": (9, 18),
            "Jueves": (9, 18),
            "Viernes": (9, 18),
            "Sábado": None,
            "Domingo": None
        },
        "Historial": [],
    },
]

turnos = []


pacientes = [
    {
        "DNI": 47130033,
        "Nombre": "Kataoka Lucas",
        "Fecha de Nacimiento": (1998, 5, 23),
        "Obra Social": "Osde",
    },
    {
        "DNI": 46120054,
        "Nombre": "Gonzalez Matias",
        "Fecha de Nacimiento": (1998, 10, 21),
        "Obra Social": "Ioma",
    },
    {
        "DNI": 48220011,
        "Nombre": "Ramirez Sofia",
        "Fecha de Nacimiento": (1994, 9, 21),
        "Obra Social": "Galeno",
    },
    {
        "DNI": 49340022,
        "Nombre": "Perez Martin",
        "Fecha de Nacimiento": (2000, 10, 9),
        "Obra Social": "Ioma",
    },
    {
        "DNI": 50450033,
        "Nombre": "Lopez Valentina",
        "Fecha de Nacimiento": (1990, 1, 7),
        "Obra Social": "Osde",
    },
    {
        "DNI": 51560044,
        "Nombre": "Torres Juan",
        "Fecha de Nacimiento": (1998, 3, 11),
        "Obra Social": "Swiss Medical",
    },
    {
        "DNI": 52670055,
        "Nombre": "Diaz Camila",
        "Fecha de Nacimiento": (1992, 11, 21),
        "Obra Social": "Ioma",
    },
    {
        "DNI": 53780066,
        "Nombre": "Fernandez Diego",
        "Fecha de Nacimiento": (1995, 10, 30),
        "Obra Social": "Galeno",
    },
    {
        "DNI": 54890077,
        "Nombre": "Morales Lucia",
        "Fecha de Nacimiento": (1993, 2, 22),
        "Obra Social": "Osde",
    },
    {
        "DNI": 55900188,
        "Nombre": "Suarez Nicolas",
        "Fecha de Nacimiento": (1999, 4, 18),
        "Obra Social": "Ioma",
    },
    {
        "DNI": 95862099,
        "Nombre": "Quijada Jesus",
        "Fecha de Nacimiento": (2003, 2, 3),
        "Obra Social": "Swiss Medical",
    }
]

especialidades_medicas = (
    "Alergología",
    "Anestesiología",
    "Cardiología",
    "Cirugía General",
    "Cirugía Cardiovascular",
    "Cirugía Plástica y Reconstructiva",
    "Cirugía Pediátrica",
    "Cirugía Torácica",
    "Cirugía Vascular",
    "Dermatología",
    "Endocrinología",
    "Gastroenterología",
    "Geriatría",
    "Ginecología y Obstetricia",
    "Hematología",
    "Hepatología",
    "Infectología",
    "Medicina de Emergencias",
    "Medicina del Deporte",
    "Medicina Familiar y Comunitaria",
    "Medicina Física y Rehabilitación",
    "Medicina Intensiva",
    "Medicina Interna",
    "Medicina Legal y Forense",
    "Nefrología",
    "Neumología",
    "Neurología",
    "Neurocirugía",
    "Nutriología Clínica",
    "Oftalmología",
    "Oncología Médica",
    "Oncología Radioterápica",
    "Ortopedia y Traumatología",
    "Otorrinolaringología",
    "Pediatría",
    "Psiquiatría",
    "Radiología",
    "Reumatología",
    "Toxicología",
    "Urología",
)

obras_y_prepagas_arg = (
    "PAMI",
    "APM / OSAPM",
    "Activa Salud",
    "Andar",
    "APRES Salud",
    "APSOT / FFST",
    "ASMEPRIV",
    "Assistravel",
    "Avalian",
    "Banco Provincia (BCO. PCIA.)",
    "Bristol / Santa Cecilia",
    "C.A.S.A",
    "CEMIC",
    "CIMA",
    "Cobermed",
    "Cobertec / OS Mosaistas",
    "Colegio de Escribanos Plan Especial (OSSEG)",
    "COMEI",
    "Corporación Asistencial",
    "DASMI - Universidad de Luján",
    "Dom Centro de Reumatología",
    "Emergencias",
    "Empleados de Farmacia",
    "OSDE",
    "Swiss Medical",
    "Medicus",
    "Omint",
    "Galeno",
    "Medifé",
    "Sancor Salud",
    "Prevención Salud",
    "Premedic",
    "Salud y Bienestar",
    "Obras Sociales Unión Personal (UP)",
    "OSVARA",
    "OSIPE",
    "Obra Social del Personal de Edificios de Renta y Horizontal",
    "Obra Social de Petroleros Privados",
    "IO SFA (Instituto de Obra Social de las Fuerzas Armadas)",
)
