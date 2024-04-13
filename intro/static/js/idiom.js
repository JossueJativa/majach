const changelanguage = async (language) => {
    try {
      // Obtener la URL del archivo actual
      if (language == null) {
        language = localStorage.getItem("language") || "es";
      }
      const requestJson = await fetch(`/static/json/languages/${language}.json`);
      const text = await requestJson.json();
  
      // Cambiar el texto de los elementos
      const elements = document.querySelectorAll('[data-section]');
      for (const element of elements) {
        const section = element.dataset.section;
        const value = element.dataset.value;
  
        element.innerHTML = text[section][value];
      }
    } catch (error) {
      console.error("Error en changelanguage:", error);
    }
};
  
function idiomchange() {
    try {
      // Saca el dataset del elemento que se clickea de los divs
      let language = event.target.parentElement.dataset.language;
      // Almacenar la selección del idioma en el almacenamiento local
      localStorage.setItem("language", language);
  
      // Cambiar el idioma
      changelanguage(language);
    } catch (error) {
      console.error("Error en idiomchange:", error);
    }
}
  
  // Cargar lenguaje al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    changelanguage();
});
  
const fileInput = document.getElementById('fileInput');
const customFileUpload = document.querySelector('.custom-file-upload');