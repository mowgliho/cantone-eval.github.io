class Manager {
  static answerInterval = 2;

  constructor(doc, div) {
    doc.create('h2','Cantone Evaluation',div);
    doc.create('hr',null,div);

    this.startDiv = this.buildStartDiv(doc, div);
    this.testDiv = this.buildTestDiv(doc, div);
    this.doneDiv = this.buildDoneDiv(doc, div);
    this.testDiv.style.display = 'none';
    this.doneDiv.style.display = 'none';

  }

  buildStartDiv(doc, parentDiv) {
    const that = this;

    let div = doc.create('div',null,parentDiv);
    doc.create('p', 'Thanks for helping out! In the following, you will see a button to play an audio file, and 6 buttons with characters on them. Please then click the character you think most corresponds to the sound heard. If the audio file is bad or sounds nothing like any of the characters, please click "NA". Your answers will be saved automatically every ' + Manager.answerInterval + ' rounds.',div);
    doc.create('hr',null,div);
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
    this.testLabel = doc.create('h3',null,div);
    let testDiv = doc.create('div',null,div);
    testDiv.style.width = '400px';
    let playButton = doc.create('button','Play', testDiv);
    doc.create('p',null,testDiv);
    let buttonDiv = doc.create('div',null,testDiv);
    this.toneButtons = {};
    for(const tone of ['NA'].concat(Tones.tones)) {
      this.toneButtons[tone] = doc.create('button',null,buttonDiv);
      this.toneButtons[tone].style.width = '14.28%'
      this.toneButtons[tone].onclick = function() { that.select(tone)};
    }
    playButton.style.width = '100%';
    playButton.onclick = function() { that.play() };

    return div;
  }

  buildDoneDiv(doc, parentDiv) {
    let div = doc.create('div',null,parentDiv);
    doc.create('h3','All done! Thanks!', div);
    return div;
  }

  getTask(id) {
    const that = this;

    this.id = id;

    let fd = new FormData();
    fd.append('id',id);

    callCgi(Config.idCgiUrl, fd, function(x) { that.startTask(x);})
  }

  play() {
    for(const button of Object.values(this.toneButtons)) button.disabled = false;
    (new Audio(Config.audioUrl + this.rounds[this.round]['fn'])).play();
  }

  startTask(data) {
    if(data['data'] == null) {
      this.errorMessage.innerHTML = 'ID not found. Are you sure that you have the right ID?';
    } else {
      this.startDiv.style.display = 'none';
      this.testDiv.style.display = 'block';
      this.doneDiv.style.display = 'none';
      this.rounds = data['data'];
      this.round = 0;
      this.answers = [];
      this.startRound();
    }
  }

  select(tone) {
    for(const button of Object.values(this.toneButtons)) button.disabled = true;
    let info = this.rounds[this.round];
    this.answers.push({
      speaker: info['speaker'],
      fn: info['fn'],
      round: info['round'],
      syl: info['syl'],
      seg: info['seg'],
      tone: info['tone'],
      rate_syl: tone == 'NA'? 'NA':info['seg'] + tone,
      rate_seg: tone == 'NA'? 'NA':info['seg'],
      rate_tone: tone == 'NA'? 'NA':tone
    });
    this.nextRound();
  }

  nextRound() {
    this.round += 1;
    if(this.round % Manager.answerInterval == 0 || this.round >= this.rounds.length) {
      this.uploadAnswers()
    } else {
      this.startNextRound()
    }
  }

  startNextRound() {
    if(this.round >= this.rounds.length) {
      this.startDiv.style.display = 'none';
      this.testDiv.style.display = 'none';
      this.doneDiv.style.display = 'block';
    } else {
      this.startRound();
    }
  }

  startRound() {
    let info = this.rounds[this.round];
    this.testLabel.innerHTML = 'Stimuli ' + (this.round + 1) + '/' + this.rounds.length;
    for(const [key,button] of Object.entries(this.toneButtons)) {
      button.innerHTML = Tones.tones.includes(key)?Tones.chars[info['seg']][key]: 'NA';
      button.disabled = true;
    }
  }

  uploadAnswers() {
    const that = this;

    let fd = new FormData();
    fd.append('id',this.id);
    fd.append('data',JSON.stringify(this.answers));

    callCgi(Config.uploadCgiUrl, fd, function(x) {
      console.log(x);
      that.answers = [];
      that.startNextRound();
    })
  }
}

window.onload = function() {
  window.AudioContext = window.AudioContext || window.webkitAudioContext;

  let div = document.getElementById('main');
  let doc = new DocumentWrapper(document);
  let manager = new Manager(doc, div);
}
