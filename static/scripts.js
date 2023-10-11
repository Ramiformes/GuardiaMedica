document.addEventListener('DOMContentLoaded', function() {

    // Inicialización de la búsqueda
    initSearch();

    // Eventos para botones .nav-link
    const buttons = document.querySelectorAll('.nav-link');
    buttons.forEach(button => {
        button.addEventListener('mousedown', function(e) {
            e.target.style.transform = 'scale(0.95)';
        });

        button.addEventListener('mouseup', function(e) {
            e.target.style.transform = 'scale(1)';
        });
    });

    // Eventos para formulaSelect
    const formulaSelect = document.getElementById('formulaSelect');
    if (formulaSelect) {
        formulaSelect.addEventListener('change', function() {
            const selectedFormula = formulaSelect.value;
            if (selectedFormula === 'cockroft_gault') {
                document.getElementById('peso').closest('.col-md-6').style.display = 'block';
                document.getElementById('raza').closest('.col-md-6').style.display = 'none';
            } else if (selectedFormula === 'ckdepi') {
                document.getElementById('peso').closest('.col-md-6').style.display = 'none';
                document.getElementById('raza').closest('.col-md-6').style.display = 'block';
            }
        });

        formulaSelect.dispatchEvent(new Event('change'));

        document.getElementById('tfgForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(e.target);
            fetch('/calcular_tfg', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('resultado').textContent = data.tfg.toFixed(2) + " mL/min";
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
// Función para cambiar el formato de la fecha
function changeDateFormat(inputDate) {
    // Divide la fecha en sus componentes
    const parts = inputDate.split('-');
    // Reorganiza en el formato dd/mm/aaaa
    return parts[2] + '/' + parts[1] + '/' + parts[0];
}

// Semanas de gestación
const gestationForm = document.getElementById('gestationForm');

if (gestationForm) {
    gestationForm.addEventListener('submit', function(e) {
        e.preventDefault();

        let fumValue = document.getElementById('fum').value;
        let ultrasoundDateValue = document.getElementById('ultrasoundDate').value;
        const ultrasoundWeeksValue = document.getElementById('ultrasoundWeeks').value;

        // Cambia el formato de las fechas
        if (fumValue) {
            fumValue = changeDateFormat(fumValue);
        }
        if (ultrasoundDateValue) {
            ultrasoundDateValue = changeDateFormat(ultrasoundDateValue);
        }

        // Validación: Asegurarse de que al menos uno de los dos métodos tenga los datos necesarios
        if (!fumValue && (!ultrasoundDateValue || !ultrasoundWeeksValue)) {
            alert('Por favor, ingrese la Fecha de Última Menstruación o ambas fechas del ultrasonido.');
            return;
        }

        const formData = new FormData(e.target);
        fetch('/calcular_gestacion', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('gestationWeeksFUM').textContent = data.weeks_fum;
                document.getElementById('gestationWeeksUltrasound').textContent = data.weeks_ultrasound;
                document.getElementById('fppFUM').textContent = data.fpp_fum;
                document.getElementById('fppUltrasound').textContent = data.fpp_ultrasound;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}


  // Función initSearch
  function initSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            console.log("Función de búsqueda activada");
            let filter = this.value.toUpperCase();
            let accordionItems = document.querySelectorAll('.accordion-item');
            console.log("Número de elementos .accordion-item:", accordionItems.length);
            accordionItems.forEach(item => {
                let linkText = item.querySelector('.link-calculadora').textContent;
                console.log("Texto del enlace:", linkText);
                if (linkText.toUpperCase().indexOf(filter) > -1) {
                    console.log("Coincidencia encontrada:", linkText);
                    item.style.display = "";
                } else {
                    console.log("Coincidencia no encontrada:", linkText);
                    item.style.display = "none";
                }
            });
        });
    }
}

const curb65Form = document.getElementById('curb65Form');
if (curb65Form) {
    curb65Form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        fetch('/calcular_curb65', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('resultadoCurb65').textContent = "Score CURB-65: " + data.score;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}

const childPughForm = document.getElementById('childPughForm');
if (childPughForm) {
    childPughForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(this);
        fetch('/calcular_childpugh', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').textContent = 'Score Child Pugh: ' + data.score;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').textContent = 'Error al calcular el score.';
        });
    });
}


//Para la calculadora de conteo absoluto de eosinófilos
const eosinofilosForm = document.getElementById('eosinofilosForm');
if (eosinofilosForm) {
    eosinofilosForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        fetch('/calcular_eosinofilos', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('resultadoEosinofilos').textContent = "Conteo Absoluto de Eosinófilos: " + data.conteo_absoluto.toFixed(2) + " x10^9/L";
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}

//Para la calculadora de IMC
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("form-imc");
    const resultado = document.getElementById("resultadoimc");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Evitar el envío tradicional del formulario

        const formData = new FormData(form);

        fetch('/calcular_imc', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.imc) {
                resultado.textContent = "Índice de masa corporal: " + data.imc.toFixed(2);
            } else if (data.error) {
                resultado.textContent = "Error: " + data.error;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            resultado.textContent = "Ocurrió un error al calcular el IMC.";
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("form-ardsnet");
    const resultado = document.getElementById("resultadoPesoPredicho");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Evitar el envío tradicional del formulario

        const formData = new FormData(form);

        fetch('/calcular_peso_predicho', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.peso_predicho) {
                resultado.textContent = "Peso predicho: " + data.peso_predicho.toFixed(2) + " kg";
            } else if (data.error) {
                resultado.textContent = "Error: " + data.error;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            resultado.textContent = "Ocurrió un error al calcular el peso predicho.";
        });
    });
});


    // Sodio corregido por glucosa
    const sodiumCorrectionForm = document.getElementById("sodiumCorrectionForm");
    const correctedSodiumSpan = document.getElementById("correctedSodium");
    const calculateButton = document.getElementById("calculateButton");

    if (calculateButton) {
        calculateButton.addEventListener("click", function(event) {
            event.preventDefault();
            const formData = new FormData(sodiumCorrectionForm);
            fetch('/correccion_sodio', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                correctedSodiumSpan.textContent = data.corrected_sodium.toFixed(2); // Mostrar con 2 decimales
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    // Superficie corporal
    const bsaCalculatorForm = document.getElementById("bsaCalculator");
    const resultSpan = document.getElementById("result");
    const calculateBSAButton = document.getElementById("calculateBSA");

    if (calculateBSAButton) {
        calculateBSAButton.addEventListener("click", function(event) {
            event.preventDefault();
            const formData = new FormData(bsaCalculatorForm);
            fetch('/bsa_calculator', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                resultSpan.textContent = data.bsa_result.toFixed(2); // Mostrar con 2 decimales
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }


// SLEDAI 2k
const sledaiForm = document.getElementById("sledaiForm");
const sledaiScoreElement = document.getElementById("sledaiScore");

if (sledaiForm) {
    sledaiForm.addEventListener("submit", function(event) {
        event.preventDefault();
        sendSLEDAIDataToServer();
    });
}

function sendSLEDAIDataToServer() {
    const formData = new FormData(sledaiForm);

    fetch('/sledai', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        sledaiScoreElement.textContent = data.score;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error al calcular la puntuación.');
    });
}






});





