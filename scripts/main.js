class Manager {
  static answerInterval = 10;

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
    doc.create('p', 'Thanks for helping out! In the following, you will see a button to play an audio file, and 6 buttons with characters on them. Please then click the character you think most corresponds to the sound heard. If the audio file is bad or sounds nothing like any of the characters, please click "NA". A screenshot of what it will look like is below', div);

    doc.create('h3', 'Screenshot: ', div);
    let image = doc.create('img',null, div);
    image.src = 'img/screenshot.png';
    image.style.border = '1px solid';

    doc.create('p', 'The system will log your answer and move automatically to the next round. Via the "Previous Stimuli" button, you will be able to go back and change your answers, and if you\'ve already answered a round you will be able to click on "Next Stimuli" move on to the next stimuli.', div)
    doc.create('p', 'Your answers will be saved automatically every ' + Manager.answerInterval + ' rounds.',div);
    doc.create('p', 'You can try it out with the evaluator ID "demo".',div);
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
    div.style.width = '400px';
    div.style.margin = 'auto';
    this.testLabel = doc.create('h3',null,div);
    let testDiv = doc.create('div',null,div);

    let playButton = doc.create('button','Play', testDiv);
    playButton.style.width = '100%';
    playButton.onclick = function() { that.play() };

    doc.create('p',null,testDiv);
    let buttonDiv = doc.create('div',null,testDiv);
    this.toneButtons = {};
    for(const tone of ['NA'].concat(Tones.tones)) {
      this.toneButtons[tone] = doc.create('button',null,buttonDiv);
      this.toneButtons[tone].style.width = '14.28%'
      this.toneButtons[tone].onclick = function() { that.select(tone)};
    }
    doc.create('p',null,testDiv);

    let backButton = doc.create('button','Previous Stimuli',testDiv);
    backButton.style.width = '50%';
    backButton.onclick = function() { that.back() };
    this.forwardButton = doc.create('button','Next Stimuli', testDiv);
    this.forwardButton.style.width = '50%';
    this.forwardButton.onclick = function() { that.forward() };

    this.savedAnswers = doc.create('p', 'Answers saved!', div);

    return div;
  }

  buildDoneDiv(doc, parentDiv) {
    let div = doc.create('div',null,parentDiv);
    this.doneMessage = doc.create('h3',null, div);
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

  back() {
    this.round = Math.max(0, this.round -1);
    this.startRound();
  }

  forward() {
    this.round += 1;
    this.startRound();
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
      this.recentlySaved = 0;
      this.answers = [];
      this.answeredRounds = new Set();
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
    this.answeredRounds.add(info['fn']);
    this.nextRound();
  }

  nextRound() {
    this.round += 1;
    if(this.answers.length == Manager.answerInterval || this.round >= this.rounds.length) {
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
      this.doneMessage.innerHTML = 'All done ' + this.id + '! Thanks!';
    } else {
      this.startRound();
    }
  }

  startRound() {
    this.recentlySaved = Math.max(0, this.recentlySaved - 1);
    let info = this.rounds[this.round];
    this.testLabel.innerHTML = 'Stimuli ' + (this.round + 1) + '/' + this.rounds.length;
    for(const [key,button] of Object.entries(this.toneButtons)) {
      button.innerHTML = Tones.tones.includes(key)?Tones.chars[info['seg']][key]: 'NA';
      button.disabled = true;
    }
    this.forwardButton.disabled = this.answeredRounds.has(info['fn'])?false: true;
    this.savedAnswers.style.display = this.recentlySaved == 0? 'none': 'block';
  }

  uploadAnswers() {
    const that = this;

    let fd = new FormData();
    fd.append('id',this.id);
    fd.append('data',JSON.stringify(this.answers));

    callCgi(Config.uploadCgiUrl, fd, function(x) {
      console.log(x);
      that.recentlySaved = 2;
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
