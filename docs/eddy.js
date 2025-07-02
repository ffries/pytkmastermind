var acc = document.getElementsByClassName("accordeon");
var i, j;

for (i = 0; i < acc.length; i++) {
	acc[i].addEventListener("click", function() {
	
    var panel = this.nextElementSibling; /*on sélectionne l'élément après this, qui doit être un panneau*/
	var isClosed = (window.getComputedStyle(panel).display === "none")
	
	/*on cache tous les panneaux*/
	for (j=0; j<acc.length; j++) {
		acc[j].nextElementSibling.style.display="none";
		acc[j].classList.remove("fonce");
	}
	
	/*on déroule ou enroule le panel*/
    if (isClosed) {
		this.classList.add("fonce");
		panel.style.display = "flex";
    }
  });
}