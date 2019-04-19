///////////////////////////////////////////
// Prediction Post and Recovery
///////////////////////////////////////////

//////////////////////////
// Live Image Post
//////////////////////////

/**
 * Submits an Ajax call with video frame if site not paused
 * recoverPrediction() handles Ajax return
 */
function postImage() {
  if (! paused) {
    var imgDataURL = grabFrame();
    $.ajax({
      type: "POST",
      url: "magic.py",
      datatype: "json",
      data: {'postData':imgDataURL},
      success: recoverPrediction
    });
  }
}

/**
 * Captures a frame from the video element and converts it
 * to a dataURL
 * @return {String} A dataURL containing the captured frame
 */
function grabFrame() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  var ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
	return canvas.toDataURL();
}

//////////////////////////
// Prediction Recovery
//////////////////////////

/**
 * Captures a frame from the video element and converts it
 * to a dataURL
 *
 * @return {String} A dataURL containing the captured frame
 */
function updateTable(predictionData) {
  if (! predictionData.face_detected || paused) {
    return;
  }
  var resultsTable = document.getElementById('resultsTable');
  var tableBody = resultsTable.getElementsByTagName('tbody')[0];
  if (tableBody.rows.length >= 4) {
    tableBody.deleteRow(-1);
  }
  var newRow = populateRow(predictionData);
  tableBody.prepend(newRow);
}


/**
 * Populates a new row element with prediction data
 *
 * @return {Object} A row element populated with prediction data
 */
function populateRow(predictionData){

  var row = document.createElement('tr');
  // var rowID = new Date().getTime();
  // row.setAttribute('id', rowID);

  var maxHeight = video.videoHeight*0.3;
  var maxWidth = video.videoWidth*0.3;

  // Cell 0
  var mids_cell = document.createElement('td');
  var mids_img = document.createElement('img');
  mids_img.src = predictionData.mids_img;
  var ratio = Math.min(maxHeight/mids_img.height, maxWidth,mids_img.width);
  mids_img.height *= ratio;
  mids_img.width *= ratio;
  mids_cell.appendChild(mids_img);
  row.appendChild(mids_cell);

  // Cell 1
  var live_cell = document.createElement('td');
  var live_img = document.createElement('img');
  live_img.height = maxHeight;
  live_img.width = maxWidth;
  live_img.src = predictionData.live_img;
  live_cell.appendChild(live_img);
  row.appendChild(live_cell);

  // Cells 2-4
  // for (let i = 0; i < 3; i++) {
  //   res_cell = document.createElement('td');
  //   let b = document.createElement('button');
  //   var br = document.createElement('br');
  //   b.setAttribute('class','btn btn-outline-primary');
  //   b.setAttribute('data-toggle','modal');
  //   b.setAttribute('data-target','#verifyModalCenter');
  //   // b.setAttribute('ontoggle', 'populateVerifyModal({predictionData.handles[i], predictionData.names[i], predictionData.live_img})');
  //   b.innerHTML = predictionData.handles[i];
  //   var confidence = document.createTextNode(predictionData.probs[i].toFixed(2));
  //   let name = document.createTextNode(predictionData.names[i]);
  //   res_cell.appendChild(b);
  //   res_cell.appendChild(confidence);
  //   res_cell.appendChild(br);
  //   res_cell.appendChild(name);
  //   b.addEventListener('click', function(){
  //     if (!paused) {
  //       pause();
  //     }
  //     $('#verifyModalImage').attr("src", predictionData.live_img);
  //     $('#verifyModalHandle').text(b.innerHTML);
  //     $('#verifyModalName').text(name.nodeValue);
  //     $('#verifyModalDegree').val(i);
  //     // postVerification(b.innerHTML, predictionData.live_img, i);
  //     // add2Dict(b.innerHTML, name.nodeValue);
  //   });
  //   row.appendChild(res_cell);
  // }
  var predictCells = [];
  for (let i = 0; i < 3; i++) {
    predictCells[i] = buildPredictionCell(predictionData.handles[i], predictionData.probs[i], predictionData.names[i]);
    let maxNeg = maxNegDegree(i);
    predictCells[i].onclick = function(){
      if (!paused) {
        pause();
      }
      $('#verifyModalImage').attr("src", predictionData.live_img);
      // console.dir(predictionData.handles);
      $('#verifyModalHandle').text(predictionData.handles[i]);
      $('#verifyModalName').text(predictionData.names[i]);
      $('#verifyModalDegree').val(i);
      $('#verifyModalNegDegree').val(maxNeg);
      $('#verifyModalNegHandle').val(predictionData.handles[maxNeg]);
      console.dir(maxNeg);
      console.dir(predictionData.handles[maxNeg]);
      // postVerification(b.innerHTML, predictionData.live_img, i);
      // add2Dict(b.innerHTML, name.nodeValue);
    }
    row.appendChild(predictCells[i]);
  }

  // Cell 5
  feedback_cell = document.createElement('td');
  var form = document.createElement('form');
  var feedback = document.createElement('input');
  feedback.setAttribute('type', 'text');
  feedback.setAttribute('placeholder', 'USNA Email');
  feedback.setAttribute('id', 'email');
  feedback.setAttribute('maxlength', '21');
  var s = document.createElement('input');
  s.setAttribute('type', 'submit');
  s.setAttribute('value', 'Submit');
  s.setAttribute('class', 'btn btn-outline-primary');
  form.appendChild(feedback);
  form.appendChild(s);
  form.onsubmit = function(e){
    if (checkEmail()) {
      $('#verifyModalHandle').text(extractHandle(checkEmail()));
      $('#verifyModalImage').attr("src", predictionData.live_img);
      $('#verifyModalName').text("");
      $('#verifyModalDegree').val(3);
      $('#verifyModalCenter').modal('show');
    } else {
      $('#invalidEmailModal').modal('show');
    }
    e.preventDefault();
    return false;
  };
  feedback_cell.appendChild(form);
  row.appendChild(feedback_cell);
  return row;
}

function buildPredictionCell(handle, confidence, name){
  var handleButton = document.createElement('button');
  var br = document.createElement('br');
  handleButton.setAttribute('class','btn btn-outline-primary');
  handleButton.setAttribute('data-toggle','modal');
  handleButton.setAttribute('data-target','#verifyModalCenter');
  handleButton.innerHTML = handle;
  var confidenceTextNode = document.createTextNode(confidence.toFixed(2));
  var nameTextNode = document.createTextNode(name);
  var res_cell = document.createElement('td');
  res_cell.appendChild(handleButton);
  res_cell.appendChild(confidenceTextNode);
  res_cell.appendChild(br);
  res_cell.appendChild(nameTextNode);
  return res_cell;
}

function maxNegDegree(degree){
  return (degree == 0 ? 1 : 0);
}

///////////////////////////////////////////
// List Generation
///////////////////////////////////////////

/**
 * Adds a new entry to the handle:name dictionary
 */
function add2Dict(handle, name) {
  handleNameDict[handle] = name;
}

/**
 * Logs the handle:name dictionary
 */
function viewListModal(){
  buildModalTable(handleNameDict);
  // console.dir(handleNameDict);
}

function buildModalTable(dict){
  var T = document.getElementById('modalTableBody');
  while (T.firstChild) {
    T.removeChild(T.firstChild);
  }
  for (var k in dict) {
    if(dict.hasOwnProperty(k)){
      var name = dict[k];
      var row = buildModalRow(k, name);
      T.appendChild(row);
    }
  }
}

function buildModalRow(user, name){
  var R = document.createElement('tr');
  var userCell = document.createElement('td');
  var nameCell = document.createElement('td');
  nameCell.innerHTML = name;
  userCell.innerHTML = user;
  R.appendChild(userCell);
  R.appendChild(nameCell);
  return R;
}

function exportList(args){
  var csv = convertDictToCSV(handleNameDict);
  if (csv == null){
    console.log("Null CSV, aborting download");
    return;
  }

  filename = args.filename || 'export.csv';

  if (!csv.match(/^data:text\/csv/i)) {
      csv = 'data:text/csv;charset=utf-8,' + csv;
  }
  data = encodeURI(csv);

  link = document.createElement('a');
  link.setAttribute('href', data);
  link.setAttribute('download', filename);
  link.click();
}

function convertDictToCSV(dict) {

  result = 'User, Last, First\n';
  for (var k in dict) {
    if(dict.hasOwnProperty(k)){
      result+= k + ',' + dict[k] + '\n';
    }
  }
  return result;
}

///////////////////////////////////////////
//
///////////////////////////////////////////
/**
* Displays Ajax return in debug span
* Calls updateTable to populate table with results
*/
function recoverPrediction(result) {
  // var out = document.getElementById("predictResult");
  // out.innerHTML = result;
  updateTable(JSON.parse(result));
}

function recoverVerify(result) {
  var out = document.getElementById("verifyResult");
  out.innerHTML = result;
}

function postVerification(handle, dataURI, degree) {
  $.ajax({
    type: "POST",
    url: "verify.py",
    datatype: "json",
    data: {'handle':handle, 'live-img':dataURI, 'degree':degree},
    success: recoverVerify
  });
}

function checkEmail() {
  var email = String(document.activeElement.parentElement.email.value);
  if (email.length < 10) {
    console.log('Invalid Email: Insufficient Length');
    return false;
  } else if (email.slice(-9) != '@usna.edu') {
    console.log('Invalid Email: Non-USNA Email Received');
    return false;
  } else {
    return email;
  }
}

function midEmail(email){
  var midEmailRegex = /m[1-2][0-9]{5}@usna.edu/;
  return midEmailRegex.test(email);
}

function extractHandle(email) {
    if (midEmail(email)) {
      // return alpha if midEmail
      var alphaRegex = /[0-9]{6}/;
      return email.match(alphaRegex);
    } else {
      // else return all text preceeding '@usna.edu'
      return email.slice(0,-9);
    }
}

function pause() {
  var activation_button = document.getElementById('activation_button');
  if (paused){
    activation_button.innerHTML = "Pause";
  }else {
    activation_button.innerHTML = "Begin";
  }
  paused = !paused;
}

// function updateTime() {
//   var date = new Date();
//   var timestamp = date.getTime();
//   var out = document.getElementById("output");
//   out.innerHTML = timestamp;
// }

function verify(){
  var handle = $('#verifyModalHandle').text();
  var name = $('#verifyModalName').text();
  var img = $('#verifyModalImage').attr('src');
  var degree = $('#verifyModalDegree').val();
  postVerification(handle, img, degree);
  add2Dict(handle, name);
}
// function populateVerifyModal(handle, name, live_img){
function populateVerifyModal(){
  console.log('yup');
  // var img = document.getElementById('verifyModalImage');
  // img.setAttribute('src', live_img);
}

///////////////////////////////////////////
// Automated Ajax call at time interval
///////////////////////////////////////////

//Interval is 1 s (1000 ms)
$(window).on('load',function(){
    $('#helpModalCenter').modal('show');
});
var handleNameDict = {};
var paused = true;
var interval = 2000;
postImage();
setInterval(postImage, interval);
