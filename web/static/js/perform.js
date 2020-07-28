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

var mainImg = document.querySelector(".mainImg");
var relatedImg = document.querySelector(".relatedImg");

var rec = [];
var curRecLen = 0;

var checkedFields = [];
var propVglMap = {};
var bookmarked = {};

var curFields;

// window.href
var hrefSplit = window.location.href.split("/");
var hrefSplitLen = hrefSplit.length;
var username = hrefSplit[hrefSplitLen - 3];
var version = hrefSplit[hrefSplitLen - 2];
var interface = hrefSplit[hrefSplitLen - 1];

//save cur answer
var curAns = "";

init();

console.log(window.screen.height, window.screen.width);

function init() {
  initFields();
  initBtns();
  generateInitRecPlots();
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
      if (interface[1] !== "4") {
        let tskId = "t" + interface[1] + "-answer";
        curAns = document.getElementById(tskId).value;
      }
    } else {
      tskModal.style.display = "block";
      displayTask();
      if (interface[1] !== "4") {
        let tskId = "t" + interface[1] + "-answer";
        curAns = document.getElementById(tskId).value;
      }
    }
  });

  tskClose.addEventListener("click", () => {
    tskModal.style.display = "none";
    if (interface[1] !== "4") {
      let tskId = "t" + interface[1] + "-answer";
      curAns = document.getElementById(tskId).value;
    }
  });

  window.addEventListener("click", (event) => {
    if (event.target == bmModal) {
      bmModal.style.display = "none";
    }
    if (event.target == tskModal) {
      tskModal.style.display = "none";
      if (interface[1] !== "4") {
        let tskId = "t" + interface[1] + "-answer";
        curAns = document.getElementById(tskId).value;
      }
    }
  });
}

function initFields() {
  fieldLst.innerHTML = "";
  let res = "";
  let url_break = window.location.href.split("/");
  let version = url_break[url_break.length - 2];
  if (version[0] === "a") {
    curFields = movieFields;
  } else {
    curFields = bsFields;
  }
  for (e of curFields.categ) {
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
  for (e of curFields.date) {
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
  for (e of curFields.quant) {
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
  // click on fields
  let fldCheckboxes = document.querySelectorAll("form .enabled div");
  for (fldcb of fldCheckboxes) {
    fldcb.addEventListener("click", clickOnField);
  }
}

function clickOnField(e) {
  let box = e.target;
  if (box != null) {
    let clickedField = box.value;
    // if a box is checked after the click
    if (box.checked) {
      // if we can check more fields add the field in.
      // also add its parsed name to the list.
      if (checkedFields.length < 3) {
        checkedFields.push(clickedField);
        // if we can not check more fields, alert it.
      } else {
        alert(`You have selected more than 3 fields!`);
        box.checked = false;
        return;
      }

      // if a box is unchecked after the click,
      // also remove its parsed name from the list.
    } else {
      checkedFields = checkedFields.filter(function (value, index, arr) {
        return value.localeCompare(clickedField) != 0;
      });
      // if 0 fields are checked, display alternative message.
      if (checkedFields.length == 0) {
        generateInitRecPlots();
        return;
      }
    }
    generatePlot(checkedFields, clickedField, box);
  }
}

function generateInitRecPlots() {
  var data = {
    data: JSON.stringify({
      fields: [],
      version: version,
    }),
  };
  $.ajax({
    async: false,
    type: "POST",
    url: "/perform_snd_flds",
    currentType: "application/json",
    data: data,
    dataType: "json",
    success: function (response) {
      console.log(response);
      mainImg.innerHTML = `No specified visualization yet. Start exploring by selecting fields on the Field panel or specifying a chart below.`;
      relatedImg.innerHTML = "";
      rec = response.recVegalite;
      for (var i = 0; i < rec.length; i++) {
        for (let prop in rec[i]) {
          let prop_str = JSON.stringify(prop).replace(/\W/g, "");
          let vglSpec = rec[i][prop];
          let sFlds = getFieldsFromVgl(vglSpec);
          let added_str = "";
          for (let fld of sFlds) {
            if (curFields.categ.includes(fld)) {
              added_str += `<i class="fas fa-font show_fld"> ${fld} </i>`;
            }
            if (curFields.quant.includes(fld)) {
              added_str += `<i class="fas fa-hashtag show_fld"> ${fld} </i>`;
            }
            if (curFields.date.includes(fld)) {
              added_str += `<i class="fas fa-calendar-alt show_fld"> ${fld} </i>`;
            }
            console.log(added_str);
          }
          relatedImg.innerHTML += `<div class='view_wrapper ${prop_str}_wrapper'> ${added_str} <i class='fas fa-bookmark add_bm' added="false"></i><i class="fas fa-list-alt specify_chart"></i><div class="views" id='${prop_str}'></div></div>`;

          vegaEmbed(`#${prop_str}`, vglSpec);
          propVglMap[prop_str] = vglSpec;
        }
      }
      document.querySelector(".loadmoreDiv").style.display = "none";
      addChartBtnsListener();
    },
  });
}

function generatePlot(checkedFields, clickedField, box) {
  console.log(checkedFields);
  var data = {
    data: JSON.stringify({
      fields: checkedFields,
      version: version,
    }),
  };
  $.ajax({
    async: false,
    type: "POST",
    url: "/perform_snd_flds",
    currentType: "application/json",
    data: data,
    dataType: "json",
    success: function (response) {
      if (response.status === "success") {
        console.log(response);
        var vglDict = response.actualVegalite;
        rec = response.recVegalite;
        for (let prop in vglDict) {
          prop_str = prop.replace(/\W/g, "");
          let added_str = "";
          checkedFields.sort();
          for (let fld of checkedFields) {
            if (curFields.categ.includes(fld)) {
              added_str += `<i class="fas fa-font show_fld"> ${fld} </i>`;
            }
            if (curFields.quant.includes(fld)) {
              added_str += `<i class="fas fa-hashtag show_fld"> ${fld} </i>`;
            }
            if (curFields.date.includes(fld)) {
              added_str += `<i class="fas fa-calendar-alt show_fld"> ${fld} </i>`;
            }
            console.log(added_str);
          }
          mainImg.innerHTML = `<div id="main_wrapper" class="view_wrapper ${prop_str}_wrapper"> ${added_str} <i class="fas fa-bookmark add_bm" added="false"></i><div class="views ${prop_str}" id="main"></div></div>`;
          let vglSpec = vglDict[prop];
          vegaEmbed("#main", vglSpec);
          propVglMap[prop_str] = vglSpec;
        }
        generateRecPlots();
      } else if (response.status === "empty") {
        // if empty chart
        alert(
          "Sorry, we cannot generate charts with the combination of selected fields."
        );
        checkedFields = checkedFields.filter(function (value, index, arr) {
          return value.localeCompare(clickedField) != 0;
        });
        box.checked = false;
      }
    },
  });
}

function generateRecPlots() {
  relatedImg.innerHTML = "";
  document.querySelector(".loadmoreDiv").style.display = "none";
  console.log(rec);
  let maxNum = 5;
  if (maxNum > rec.length) {
    maxNum = rec.length;
  }
  for (var i = 0; i < rec.length; i++) {
    for (let prop in rec[i]) {
      let prop_str = JSON.stringify(prop).replace(/\W/g, "");

      let vglSpec = rec[i][prop];
      vegaEmbed(`#${prop_str}`, vglSpec);
      let sFields = getFieldsFromVgl(vglSpec);
      console.log(sFields);
      let added_str = "";
      for (let fld of sFields) {
        if (curFields.categ.includes(fld)) {
          added_str += `<i class="fas fa-font show_fld"> ${fld} </i>`;
        }
        if (curFields.quant.includes(fld)) {
          added_str += `<i class="fas fa-hashtag show_fld"> ${fld} </i>`;
        }
        if (curFields.date.includes(fld)) {
          added_str += `<i class="fas fa-calendar-alt show_fld"> ${fld} </i>`;
        }
      }

      relatedImg.innerHTML += `<div class='view_wrapper ${prop_str}_wrapper'> ${added_str} <i class='fas fa-bookmark add_bm' added="false"></i><i class="fas fa-list-alt specify_chart"></i><div class="views" id='${prop_str}'></div></div>`;

      propVglMap[prop_str] = vglSpec;
      if (i >= maxNum) {
        document.querySelector(`.${prop_str}_wrapper`).style.display = "none";
      }
    }
  }
  addChartBtnsListener();

  if (rec.length > 5) {
    curRecLen = 5;
    document.querySelector(".loadmoreDiv").style.display = "block";
    document
      .querySelector("#loadmoreBtn")
      .addEventListener("click", loadMoreRec);
  }
}

function loadMoreRec() {
  console.log("click loadmore.");
  let maxNum = curRecLen + 5;
  if (maxNum >= rec.length) {
    maxNum = rec.length;
    document.querySelector(".loadmoreDiv").style.display = "none";
  }
  for (var i = curRecLen; i < maxNum; i++) {
    for (let prop in rec[i]) {
      let prop_str = JSON.stringify(prop).replace(/\W/g, "");
      document.querySelector(`.${prop_str}_wrapper`).style.display = "block";
    }
  }
  // addChartBtnsListener();
  curRecLen = maxNum;
}

function specifyChart(e) {
  let vis = e.target.parentElement;
  let prop_str = vis.classList.item(1).split("_wrapper")[0];
  let vglSpec = propVglMap[prop_str];

  reassignFields(vglSpec);

  var data = {
    data: JSON.stringify({
      vgl: vglSpec,
      version: version,
    }),
  };
  $.ajax({
    async: false,
    type: "POST",
    url: "/perform_snd_spcs",
    currentType: "application/json",
    data: data,
    dataType: "json",
    success: function (response) {
      console.log(response);
      rec = response.recVegalite;

      let sFields = getFieldsFromVgl(vglSpec);
      console.log(sFields);
      let added_str = "";
      for (let fld of sFields) {
        if (curFields.categ.includes(fld)) {
          added_str += `<i class="fas fa-font show_fld"> ${fld} </i>`;
        }
        if (curFields.quant.includes(fld)) {
          added_str += `<i class="fas fa-hashtag show_fld"> ${fld} </i>`;
        }
        if (curFields.date.includes(fld)) {
          added_str += `<i class="fas fa-calendar-alt show_fld"> ${fld} </i>`;
        }
      }

      mainImg.innerHTML = `<div id="main_wrapper" class="view_wrapper ${prop_str}_wrapper"> ${added_str} <i class="fas fa-bookmark add_bm" added="false"></i><div class="views ${prop_str}" id="main"></div></div>`;

      vegaEmbed("#main", vglSpec);
      generateRecPlots();
    },
  });
}

function reassignFields(vgljson) {
  console.log(vgljson);
  let all_boxes = document.querySelectorAll(".form-check-input");
  console.log(all_boxes);

  let fields = getFieldsFromVgl(vgljson);

  for (box of all_boxes) {
    // console.log(box.value);
    if (fields.includes(box.value)) {
      box.checked = true;
    } else {
      box.checked = false;
    }
  }
  checkedFields = fields;
}

function addChartBtnsListener() {
  // add event listeners to all bookmark buttons on the page
  let btns = document.querySelectorAll(".add_bm");
  for (btn of btns) {
    btn.addEventListener("click", toggleBookMark);
  }

  let specBtns = document.querySelectorAll(".specify_chart");
  for (sBtn of specBtns) {
    sBtn.addEventListener("click", specifyChart);
  }

  let wrappers = document.querySelectorAll(".view_wrapper");

  // change color and state of a bookmark if a wrapper is in the bookmark content.
  for (wrapper of wrappers) {
    let item = `${wrapper.classList.item(1).split("_wrapper")[0]}`;
    if (item in bookmarked) {
      wrapper.querySelector("i").style.color = "#ffa500";
      wrapper.querySelector("i").setAttribute("added", "true");
    }
  }
}

function toggleBookMark(e) {
  let btn = e.target;
  let vis = e.target.parentElement;
  let str = vis.classList.item(1);
  // if the mark was checked, user want to uncheck it.
  if (btn.getAttribute("added") == "true") {
    // remove bookmark from pop up window
    let arr = bookmarkContent.childNodes;
    for (n of arr) {
      if (
        `${str}`
          .split("_wrapper")[0]
          .split("_bm")[0]
          .localeCompare(n.classList.item(1).split("_bm")[0]) == 0
      ) {
        bookmarkContent.removeChild(n);
      }
    }
    delete bookmarked[`${str.split("_wrapper")[0]}`];

    // change color and state of the plot in views
    let mark = document.querySelector(`.${str.split("_bm")[0]} .add_bm`);
    if (mark != null) {
      mark.style.color = "rgb(216, 212, 223)";
      mark.setAttribute("added", "false");
    }
    refreshBookmark();

    // if the mark is unchecked, user want to check it.
  } else {
    btn.style.color = "#ffa500";
    btn.setAttribute("added", "true");

    let splittedStr = `${str.split("_wrapper")[0]}`;

    bookmarked[splittedStr] = propVglMap[splittedStr];
    refreshBookmark();
  }
}

function refreshBookmark() {
  let btnstrs = [];

  if (Object.keys(bookmarked).length == 0) {
    bookmarkContent.innerHTML =
      "Oops, you don't have any bookmark yet. Click on bookmark tags on charts to add a bookmark!";
  } else {
    bookmarkContent.innerHTML = "";
    for (key of Object.keys(bookmarked)) {
      let value = bookmarked[key];
      console.log(bookmarked);
      console.log(key);

      let sFields = getFieldsFromVgl(propVglMap[key]);
      console.log(sFields);
      let added_str = "";
      for (let fld of sFields) {
        if (curFields.categ.includes(fld)) {
          added_str += `<i class="fas fa-font show_fld"> ${fld} </i>`;
        }
        if (curFields.quant.includes(fld)) {
          added_str += `<i class="fas fa-hashtag show_fld"> ${fld} </i>`;
        }
        if (curFields.date.includes(fld)) {
          added_str += `<i class="fas fa-calendar-alt show_fld"> ${fld} </i>`;
        }
      }

      // creat div structure append to the popup window.
      bookmarkContent.innerHTML += `<div class="view_wrapper ${key}_wrapper_bm" > ${added_str} <i class="fas fa-bookmark add_bm" added="true"></i><div class="views" id="${key}_bm"></div></div>`;

      // plot the recommandation
      vegaEmbed(`#${key}_bm`, value);

      btnstrs.push(`.${key}_wrapper_bm .add_bm`);
      let btn = document.querySelector(`.${key}_wrapper_bm .add_bm`);

      // change color and attribute of bookmark.
      btn.style.color = "#ffa500";
      btn.setAttribute("added", "true");
    }
    // add event listener to new bookmark
    for (btn of btnstrs)
      document.querySelector(btn).addEventListener("click", toggleBookMark);
  }
}

function displayTask() {
  if (version[0] === "a" && interface[1] === "1") {
    taskContent.innerHTML =
      "<div><b>Question:</b> Which creative type has the highest average IMDB Rating?<br> Please <b>enter your answer</b> and also <b>bookmark charts</b> you think that could answer the question. <br><br><label>Your answer:</label> &nbsp;&nbsp; <input type='text' id='t1-answer'><br> <input type='checkbox' id='t1-complete-bm' /> &nbsp;&nbsp; <label>I have also bookmarked the charts which I think they could answer the quesion.</label><br><button type='button' class='btn btn-sm btn-outline-dark' onclick='goPostTaskQuest()'> Submit, then go to next step.</button></div>";
  } else if (version[0] === "a" && interface[1] === "2") {
    taskContent.innerHTML =
      "<div><b>Question:</b> Which genre has higher average rotten tomatoes rating, Adventure, or Horror?<br> Please <b>enter your answer</b> and also <b>bookmark charts</b> you think that could answer the question. <br><br><label>Your answer:</label> &nbsp;&nbsp; <input type='text' id='t2-answer'><br> <input type='checkbox' id='t2-complete-bm' /> &nbsp;&nbsp; <label>I have also bookmarked the charts which I think they could answer the quesion.</label><br><button type='button' class='btn btn-sm btn-outline-dark' onclick='goPostTaskQuest()'> Submit, then go to next step.</button></div>";
  } else if (version[0] === "a" && interface[1] === "3") {
    taskContent.innerHTML =
      "<div><b>Question:</b> What kinds of movies will be the most successful movies based on your observations of the data? Summarize the 2-3 characteristics that you believe are most important in predicting their success.<br> Please <b>enter your answer</b> and also <b>bookmark charts</b> you think that could answer the question. <br><br><label>Your answer:</label> &nbsp;&nbsp; <textarea id='t3-answer' rows='2' cols='50'></textarea><br> <input type='checkbox' id='t3-complete-bm' /> &nbsp;&nbsp; <label>I have also bookmarked the charts which I think they could answer the quesion.</label><br><button type='button' class='btn btn-sm btn-outline-dark' onclick='goPostTaskQuest()'> Submit, then go to next step.</button></div>";
  } else if (version[0] === "a" && interface[1] === "4") {
    taskContent.innerHTML =
      "<div><b>Question:</b> Feel free to explore any and all aspects of the data for <b>[15 mins]</b>. Use the bookmark features to save any interesting patterns, trends or other insights worth sharing with colleagues. Note the top 3 bookmarks that you found most interesting from your exploration.<br> Please <b>bookmark top 3 charts</b> you think that could answer the question. <br><br> <input type='checkbox' id='t4-complete-bm' /> &nbsp;&nbsp; <label>I have also bookmarked the charts which I think they could answer the quesion.</label><br><button type='button' class='btn btn-sm btn-outline-dark' onclick='goPostTaskQuest()'> Submit, then go to next step.</button></div>";
  }
}

function goPostTaskQuest() {
  let ansId, cmpBMId, answer, cmplBMChecked;
  if (interface[1] !== "4") {
    ansId = "t" + interface[1] + "-answer";
    answer = document.getElementById(ansId).value;
  }

  cmpBMId = "t" + interface[1] + "-complete-bm";
  cmplBMChecked = document.getElementById(cmpBMId).checked;
  // check if bookmarked list empty or not
  if (interface[1] == 4) {
    if (Object.keys(bookmarked).length != 3) {
      alert("You could only bookmark 3 charts for this task.");
      return;
    }
  } else {
    if (Object.keys(bookmarked).length == 0) {
      alert(
        "Please bookmark charts that you think they could answer the question."
      );
      return;
    }
  }
  // check answer and checkbox
  if (interface[1] === "4") {
    if (cmplBMChecked == false) {
      alert("Please tick the checkbox.");
      return;
    } else {
      window.location =
        "/" + username + "/" + version + "/" + "q" + interface[1];
    }
  } else {
    if (answer === "" || cmplBMChecked == false) {
      alert("Please answer the question and tick the checkbox.");
      return;
    } else {
      window.location =
        "/" + username + "/" + version + "/" + "q" + interface[1];
    }
  }
}

function getFieldsFromVgl(vgl) {
  var flds = [];
  for (encode in vgl["encoding"]) {
    if ("field" in vgl["encoding"][encode]) {
      flds.push(vgl["encoding"][encode]["field"]);
    }
  }
  flds.sort();
  return flds;
}
