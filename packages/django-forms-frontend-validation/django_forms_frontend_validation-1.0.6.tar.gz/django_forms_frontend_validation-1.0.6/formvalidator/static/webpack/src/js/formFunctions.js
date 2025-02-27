// ########## Getting the csrf token for the fetch calls ##########
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
export const csrftoken = getCookie('csrftoken');

// ##### Fetch Calls #####
// performs fetch call to view
export const fetchHandleForm = async (form) => {
    let formData = new FormData(form);
    return await fetch(form.action, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            // "Accept": "m",
            // "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
        },
        body: formData,
    }).then(async (response) => {
        return response.json();
    });
}
// ***** Adding asterisks to labels of required inputs *****
function addAsterisks(form) {
    // gathering all inputs
    let formGroups = document.querySelectorAll(`#${form.id} .form-group`);
    let inputs = getRequiredFields(formGroups);

    // adding the required-field class which will add the asterisk
    for (let i = 0; i < inputs.length; i++) {
        let label = document.querySelector(`label[for=${inputs[i].name}]`);
        if (inputs[i].required) {
            label.classList.add("required-field");
        }
    }
}

// In-line validation on required fields
function validateInputs(form) {
    // gathering all inputs
    let formGroups = document.querySelectorAll(`#${form.id} .form-group`);
    let inputs = getRequiredFields(formGroups);

    // adding listeners to each input for validation
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener("focusout", () => {
            if (inputs[i].value === "" || inputs[i].value === null) {
                addError(inputs[i]);
            } else {
                removeError(inputs[i]);
            }
        });
    }
}
// validateInputs();

// check form function
export function checkForm(form) {
    let errors = false;

    // gathering all inputs
    let formGroups = document.querySelectorAll(`#${form.id} .form-group`);
    let inputs = getRequiredFields(formGroups);

    // iterating through all required fields to check for invalidation
    for (let i = 0; i < inputs.length; i++) {
        let input = inputs[i];
        if (input.value === "" || !input.value) {
            addError(input);
            errors = true;
        }
    }

    return errors
}

// submit button validation check
function submitValidation(form) {
    form.form.addEventListener("submit", (e) => {
        // preventing default submission behavior
        e.preventDefault();

        // gathering all inputs
        let f = e.target;
        // let formGroups = document.querySelectorAll(`#${form.id} .form-group`);
        // let inputs = getRequiredFields(formGroups);
        // // let form = document.getElementById("form") !== null ? document.getElementById("form") : document.getElementById("userForm");
        let errors = checkForm(f);

        // submitting the form if there aren't any errors
        if (!errors) {
            form.form.submit();
        } else {
            let invalidInputs = document.getElementsByClassName("validation-error");
            // scroll to the first invalid input
            invalidInputs[0].parentElement.scrollIntoView();
        }
    });
}

// adds an error to an input
function addError(input) {
    let inputParent = input.parentElement;
    if (!inputParent.className.includes("form-group")){
        inputParent = input.parentElement.parentElement;
    }
    let errorAdded = inputParent.dataset.errorAdded;
    inputParent.classList.add("validation-error");
    input.classList.add("error-input")
    if (errorAdded === "false" || !errorAdded) {
        // creating the error message p
        let eP = document.createElement("p");
        eP.setAttribute("class", "error-msg");
        eP.innerText = "This input is required";
        inputParent.appendChild(eP);
        inputParent.dataset.errorAdded = "true";
    }
}

// removes the error from an input
function removeError(input) {
    let inputParent = input.parentElement;
    if (!inputParent.className.includes("form-group")){
        inputParent = input.parentElement.parentElement;
    }
    let errorAdded = inputParent.dataset.errorAdded;
    inputParent.classList.remove("validation-error");
    input.classList.remove("error-input");
    // removing the error message p
    if (errorAdded === "true") {
        inputParent.removeChild(inputParent.lastElementChild);
        inputParent.dataset.errorAdded = "false";
    }
}

// function to get all required input
function getRequiredFields(formGroups) {
    let nameList = ["SELECT", "INPUT", "TEXTAREA"];
    let inputs = [];
    // let formGroups = document.getElementsByClassName("form-group");
    for (let i = 0; i < formGroups.length; i++) {
        let children = formGroups[i].children;
        for (let j = 0; j < children.length; j++) {
            if (children[j].tagName === "DIV"){
                let grandChildren = children[j].children;
                for (let a = 0; a < grandChildren.length; a++) {
                    if (nameList.includes(grandChildren[a].tagName)) {
                        if (grandChildren[a].required) {
                            inputs.push(grandChildren[a]);
                        }
                    }
                }
            }
            else{
                if (nameList.includes(children[j].tagName)) {
                    if (children[j].required) {
                        inputs.push(children[j]);
                    }
                }
            }
        }
    }
    return inputs
}

// checks if the form will be ignored form validation.
function getIgnored(form, ignoredClasses) {
    let isIgnored = false;
    let classes = form.classList;
    if (ignoredClasses.length > 0) {
        classes.forEach((_class) => {
            if (ignoredClasses.includes(_class)) {
                isIgnored = true;
                return isIgnored;
            }
        });
    }
    return isIgnored
}

// Checks if the form will be validated.
function isValidate(form, ignoredClasses) {
    let enableValidate = true;
    let classes = form.classList;
    if (ignoredClasses.length > 0) {
        classes.forEach((_class) => {
            if (ignoredClasses.includes(_class)) {
                enableValidate = false;
                return enableValidate;
            }
        });
    }
    return enableValidate
}

// Confirms if a form will only validate the form on submit, only.
function getValidateOnlyValidateOnSubmit(form, validateOnlyOnSubmit, enableValidation) {
    let validateOnSubmit = false;
    let trueFlags = ["all", "__all__", "*", "true"];
    if (enableValidation) {
        let classes = form.classList;
        if (trueFlags.includes(validateOnlyOnSubmit[0])) {
            validateOnSubmit = true;
            return true;
        }
        else {
            classes.forEach((_class) => {
                if (validateOnlyOnSubmit.includes(_class)) {
                    validateOnSubmit = true;
                    return validateOnlyOnSubmit;
                }
            });
        }
    }
    return validateOnSubmit;
}

// adds listener logic to the form
export function _Initialize(form={}){
    if (!form.ignored || form.enableValidation) {
        // add all listeners to each form
        addAsterisks(form);
        if (!form.validateOnlyOnSubmit) {
            validateInputs(form);
        }
        if (!form.ignored) {
            submitValidation(form);
        }
    }
}

// function to initialize forms into a json object
export function _InitializeForms(formNodes, ignoredFormClasses=[], ignoredValidationClasses=[], validateOnlyOnSubmit){
    for (let i = 0; i < formNodes.length; i++) {
        let currentForm = formNodes[i];
        let ignored = getIgnored(currentForm, ignoredFormClasses);
        let enableValidation = isValidate(currentForm, ignoredValidationClasses);
        let validateOnSubmit = getValidateOnlyValidateOnSubmit(currentForm, validateOnlyOnSubmit, enableValidation);
        let _form = {
            id: currentForm.id,
            form: currentForm,
            ignored: ignored,
            enableValidation: enableValidation,
            validateOnlyOnSubmit: validateOnSubmit,
        }

        // adding form functionality
        _Initialize(_form);
    }
}