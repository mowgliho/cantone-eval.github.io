class Manager {

  constructor(doc, div) {
    doc.create('h2','Cantone Evaluation',div);
    doc.create('hr',null,div);

    this.startDiv = this.buildStartDiv(doc, div);
    this.testDiv = this.buildTestDiv(doc, div);
    this.testDiv.style.display = 'none';

  }

  buildStartDiv(doc, parentDiv) {
    const that = this;

    let div = doc.create('div',null,parentDiv);
    doc.create('label','What is your evaluator ID? ',div);
    let input = doc.create('input',null,div);
    input.type = 'text';
    let button = doc.create('button', 'Submit', div);
    button.onclick = function() { that.getTask(input.value)};
    this.errorMessage = doc.create('p', null, div);
    this.errorMessage.style.color = 'red';
    return div;
  }

  buildTestDiv(doc, parentDiv) {
    const that = this;

    let div = doc.create('div',null,parentDiv);
    return div;
  }

  getTask(id) {
    if(false) {
      this.startDiv.style.display = 'none';
      this.testDiv.style.display = 'visible';
      this.update();
    } else {
      this.errorMessage.innerHTML = 'Failed to get ID info. Make sure that you didn\'t type it in wrong!'
    }
  }

}
window.onload = function() {
  window.AudioContext = window.AudioContext || window.webkitAudioContext;

  let div = document.getElementById('main');
  let doc = new DocumentWrapper(document);
  let manager = new Manager(doc, div);
}
