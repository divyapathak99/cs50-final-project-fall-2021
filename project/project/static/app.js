console.log("Welcome to muggle notes app. This is app.js");
showNotes();

// If user adds a note and title, add it to the localStorage
let addBtn = document.getElementById("addBtn");
addBtn.addEventListener("click", function(e) {
  var today = new Date();
  var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
  var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  var dateTime = date+' '+time;
  let addTxt = document.getElementById("addTxt");
  let addtitle = document.getElementById("addtitle");

  // user specific localStorage
  if(addTxt.value != "" && addtitle.value != ""){
      let notes = localStorage.getItem("notes"+name);
      let dates = localStorage.getItem("dates"+name);
      let titles = localStorage.getItem("titles"+name);

  // if null then create an empty array
  if (notes == null && titles == null && dates == null) {
    notesObj = [];
    titlesObj = [];
    datesObj = [];
  }
  // otherwise get all the local storage in an array.
  else {
    notesObj = JSON.parse(notes);
    titlesObj = JSON.parse(titles);
    datesObj =  JSON.parse(dates);
  }
  notesObj.push(addTxt.value);
  titlesObj.push(addtitle.value);
  datesObj.push(dateTime);
  // Set the local storage Key
  localStorage.setItem("notes"+name, JSON.stringify(notesObj));
  localStorage.setItem("titles"+name, JSON.stringify(titlesObj));
  localStorage.setItem("dates"+name, JSON.stringify(datesObj));
  addTxt.value = "";
  addtitle.value = "";
//   console.log(notesObj);
  showNotes();
  }

});

// Function to show elements from localStorage
function showNotes() {
  let notes = localStorage.getItem("notes"+name);
  let titles = localStorage.getItem("titles"+name);
  let dates = localStorage.getItem("dates"+name);
  let Impnotes = localStorage.getItem("Impnotes"+name);

  if (notes == null && titles == null && dates == null) {
      notesObj = [];
      titlesObj = [];
      datesObj = [];
   } else {
     notesObj = JSON.parse(notes);
     titlesObj = JSON.parse(titles);
     datesObj = JSON.parse(dates);
  }
  if (Impnotes == null){
      ImpnotesObj = [];
  }else{
      ImpnotesObj = JSON.parse(Impnotes);
  }
  let html = "";
  notesObj.forEach(function(element, index) {

      // Checking if the note is imporatant
      if (ImpnotesObj.includes(titlesObj[index])){
           html += `
            <div class="noteCard my-2 mx-2 card" style="width: 18rem;">
                  <div class="card-header bg-danger">
                        <h5 class="card-title">${titlesObj[index]}</h5>
                        <h9 style="color: black">${datesObj[index]}</h9>
                  </div>
                  <div class="card-body bg-danger">
                        <p class="card-text"> ${element}</p>
                        <button id="${index}"onclick="deleteNote(this.id)" class="btn btn-primary">Delete Note</button>
                        <button id="imp_${index}"onclick="ImpNote(this.id)" class="btn btn-primary">Imp Note</button>
                    </div>
                </div>`;
      }else{
          html += `
            <div class="noteCard my-2 mx-2 card" style="width: 18rem;">
                    <div class="card-header bg-success">
                        <h5 class="card-title">${titlesObj[index]}</h5>
                        <h9 style="color: black">${datesObj[index]}</h9>
                  </div>
                  <div class="card-body bg-success">
                        <p class="card-text"> ${element}</p>
                        <button id="${index}"onclick="deleteNote(this.id)" class="btn btn-primary">Delete Note</button>
                        <button id="imp_${index}"onclick="ImpNote(this.id)" class="btn btn-primary">Imp Note</button>
                    </div>
                </div>`;
      }
  });
  let notesElm = document.getElementById("notes");
  if (notesObj.length != 0) {
    notesElm.innerHTML = html;
  } else {
    notesElm.innerHTML = `Nothing to show! Use "Add a Note" section above to add notes.`;
  }
}

// Function to delete a note
function deleteNote(index) {
//   console.log("I am deleting", index);

  let notes = localStorage.getItem("notes"+name);
  let titles = localStorage.getItem("titles"+name);
  let dates = localStorage.getItem("dates"+name);
  let Impnotes = localStorage.getItem("Impnotes"+name);
  if (notes == null && titles == null  && dates == null) {
    notesObj = [];
    titlesObj = [];
    datesObj = [];
  } else {
    notesObj = JSON.parse(notes);
    titlesObj = JSON.parse(titles);
    datesObj = JSON.parse(dates);
  }
  if(Impnotes == null){
      ImpnotesObj = [];
  }else{
      ImpnotesOnj = JSON.parse(Impnotes)
  }

  if (ImpnotesObj.includes(titlesObj[index])){
      console.log("yes");
      let x = ImpnotesObj.indexOf(titlesObj[index]);
      ImpnotesObj.splice(x,1);
      localStorage.setItem("Impnotes"+name, JSON.stringify(ImpnotesObj));
  }
  notesObj.splice(index, 1);
  datesObj.splice(index, 1);
  titlesObj.splice(index, 1);

  localStorage.setItem("notes"+name, JSON.stringify(notesObj));
  localStorage.setItem("titles"+name, JSON.stringify(titlesObj));
  localStorage.setItem("dates"+name, JSON.stringify(datesObj));
  showNotes();
}


// function for search a note by its content.
let search = document.getElementById('searchTxt');
search.addEventListener("input", function(){

    let inputVal = search.value.toLowerCase();
    // console.log('Input event fired!', inputVal);
    let noteCards = document.getElementsByClassName('noteCard');
    Array.from(noteCards).forEach(function(element){
        let cardTxt = element.getElementsByTagName("p")[0].innerText;
        if(cardTxt.toLowerCase().includes(inputVal)){
            element.style.display = "block";
        }
        else{
            element.style.display = "none";
        }
        // console.log(cardTxt);
    })
})

// creating a lolcal storage for important note that will store titles for important notes
function ImpNote(index){
    const x = index.split("_")[1];
  let Impnotes = localStorage.getItem("Impnotes"+name);
  let titles = localStorage.getItem("titles"+name);

  if (titles == null) {
    titlesObj = [];
  } else {
    titlesObj = JSON.parse(titles);
  }
  if(Impnotes == null){
      ImpnotesObj = [];
  }else{
      ImpnotesObj = JSON.parse(Impnotes);
  }

  // Checking it a note is already important
  if (ImpnotesObj.includes(titlesObj[x]) == false){
      ImpnotesObj.push(titlesObj[x]);
      localStorage.setItem("Impnotes"+name, JSON.stringify(ImpnotesObj));
  }
  showNotes();
}
