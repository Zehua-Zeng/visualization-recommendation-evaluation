// dataset fields
var movieFields = {
  categ: [
    "Creative_Type",
    "Director",
    "Distributor",
    "Major_Genre",
    "MPAA_Rating",
    "Source",
    "Title",
  ],
  date: ["Release_Date"],
  quant: [
    "IMDB_Rating",
    "IMDB_Votes",
    "Production_Budget",
    "Rotten_Tomatoes_Rating",
    "Running_Time_min",
    "US_DVD_Sales",
    "US_Gross",
    "Worldwide_Gross",
  ],
};

var bsFields = {
  categ: [
    "Aircraft_Airline_Operator",
    "Aircraft_Make_Model",
    "Airport_Name",
    "Effect_Amount_of_damage",
    "Origin_State",
    "When_Phase_of_flight",
    "When_Time_of_day",
    "Wildlife_Size",
    "Wildlife_Species",
  ],
  date: ["Flight_Date"],
  quant: ["Cost_Other", "Cost_Repair", "Cost_Total_$", "Speed_IAS_in_knots"],
};

// global vars
var bookmarkContent = document.querySelector(".bookmark_content");
var taskContent = document.querySelector(".task_content");
var fieldLst = document.querySelector(".attr-lst");

init();

function init() {
  initFields();
  initBtns();
}

function initBtns() {
  let bmModal = document.querySelector("#bmpopup");
  let bmBtn = document.querySelector("#bookmark");
  let bmClose = document.querySelector("#bmclose");

  let tskModal = document.querySelector("#tskpopup");
  let tskBtn = document.querySelector("#task");
  let tskClose = document.querySelector("#tskclose");

  bmBtn.addEventListener("click", () => {
    if (bmModal.style.display == "block") {
      bmModal.style.display = "none";
    } else {
      bmModal.style.display = "block";
      refreshBookmark();
    }
  });

  bmClose.addEventListener("click", () => {
    bmModal.style.display = "none";
  });

  tskBtn.addEventListener("click", () => {
    if (tskModal.style.display == "block") {
      tskModal.style.display = "none";
    } else {
      tskModal.style.display = "block";
      displayTask();
    }
  });

  tskClose.addEventListener("click", () => {
    tskModal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target == bmModal) {
      bmModal.style.display = "none";
    }
    if (event.target == tskModal) {
      tskModal.style.display = "none";
    }
  });
}

function initFields() {
  let fields;
  fieldLst.innerHTML = "";
  let res = "";
  let url_break = window.location.href.split("/");
  let version = url_break[url_break.length - 2];
  if (version[0] === "a") {
    fields = movieFields;
  } else {
    fields = bsFields;
  }
  for (e of fields.categ) {
    res += `<li class="categ-attr enabled">
                    <div>
                        <i class="fas fa-font"></i> &nbsp;
                        <label class="form-check-label" for="${e}">
                           ${e}
                        </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}"/>
                        </span>
                    </div>
                </li>`;
  }
  for (e of fields.date) {
    res += `<li class="date-attr enabled">
                    <div>
                        <i class="fas fa-calendar-alt"></i> &nbsp;
                        <label class="form-check-label" for="${e}"> ${e} </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}" />
                        </span>
                    </div>
                </li>`;
  }
  for (e of fields.quant) {
    res += `<li class="quant-attr enabled">
                    <div>
                        <i class="fas fa-hashtag"></i> &nbsp;
                        <label class="form-check-label" for="${e}"> ${e} </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}" />
                        </span>
                    </div>
                </li>`;
  }
  fieldLst.innerHTML += res;
  let a = document.querySelectorAll("form .enabled div");
  for (i of a) {
    i.addEventListener("click", clickOnField);
  }
}

function clickOnField(e) {}

function refreshBookmark() {
  bookmarkContent.innerHTML =
    "Oops, you don't have any bookmark yet. Click on bookmark tags on charts to add a bookmark!";
}

function displayTask() {
  taskContent.innerHTML =
    "<div><b>Question:</b> Which creative type has the highest average IMDB Rating?<br> Please <b>enter your answer</b> and also <b>bookmark charts</b> you think that could answer the question. <br><br><label>Your answer:</label> &nbsp;&nbsp; <input type='text' id='t1-answer'><br> <input type='checkbox' id='complete-bm' /> &nbsp;&nbsp; <label>I have also bookmarked the charts which could answer the quesion.</label><br><a class='btn btn-outline-dark' href='/{{ version }}/t2' role='button'>Submit, then go to next task.</a></div>";
}
