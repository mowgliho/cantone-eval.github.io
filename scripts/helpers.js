class DocumentWrapper {
  constructor(doc) {
    this.doc = doc;
  }

  create(type, html, div) {
    let ret = this.doc.createElement(type);
    if (typeof html !== 'undefined' && html != null) ret.innerHTML = html;
    if (typeof div !== 'undefined' && div != null) div.appendChild(ret);
    return ret;
  }
}

callCgi = function(url, body, callback) {
  fetch(url, { method: 'POST', body: body}).then(
    (response) => {response.text().then(function(x) {
      callback(JSON.parse(x));
    })}).catch(
    (error) => {console.log("error", error)});
}


