Survey.StylesManager.applyTheme("modern");

function resultHandlerBuilder(name) {
  return function (result) {
    fetch("/api/results/" + name, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(result.data),
    })
      .then((response) => response.json())
      .then((data) => {
        var elem = document.createElement("h3");
        elem.innerHTML = "Your survey completion code is: " + data.code;
        var completed = document.getElementsByClassName("sv-completedpage")[0];
        completed.appendChild(elem);
      })
      .catch((err) => {
        var elem = document.createElement("h3");
        elem.innerHTML = "Your survey completion code is: 999960";
        var completed = document.getElementsByClassName("sv-completedpage")[0];
        completed.appendChild(elem);
      });
  };
}

function load_survey(name) {
  form_promise = fetch("/surveys/" + name + ".json");

  window.onload = function () {
    form_promise
      .then((res) => res.json())
      .then((out) => {
        json = out;
        window.survey = new Survey.Model(json);
        survey.render("surveyElement");
        survey.onComplete.add(resultHandlerBuilder(name));
      })
      .catch((err) => (window.location = "/404"));
  };
}
