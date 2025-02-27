/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else if(typeof exports === 'object')
		exports["fv"] = factory();
	else
		root["fv"] = factory();
})(this, () => {
return /******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./node_modules/css-loader/dist/cjs.js!./src/css/style.css":
/*!*****************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./src/css/style.css ***!
  \*****************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_css_loader_dist_runtime_noSourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/noSourceMaps.js */ \"./node_modules/css-loader/dist/runtime/noSourceMaps.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_noSourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_noSourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/api.js */ \"./node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);\n// Imports\n\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_noSourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));\n// Module\n___CSS_LOADER_EXPORT___.push([module.id, `/****** Forms ******/\r\ninput, select {\r\n  font-size: 18px!important;\r\n}\r\n\r\n.errorlist li, .error-msg {\r\n    color: red;\r\n}\r\n\r\n.error {\r\n  color: red;\r\n  font-style: italic;\r\n}\r\n\r\n.error-input {\r\n  background: #edbabf;\r\n  border-color: #dc3545;\r\n}\r\n\r\n.error-msg {\r\n  color: #dc3545;\r\n  margin-bottom: 0;\r\n}\r\n\r\n.success {\r\n  color: blue;\r\n}\r\n\r\n.readonly {\r\n  background-color: #e9ecef;\r\n  opacity: 1;\r\n  cursor: not-allowed;\r\n}\r\n\r\n.required-field {\r\n    font-weight: 800;\r\n}\r\n\r\n.required-field::after {\r\n  content: \" *\";\r\n  color: red;\r\n}`, \"\"]);\n// Exports\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack://fv/./src/css/style.css?./node_modules/css-loader/dist/cjs.js");

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

eval("\n\n/*\n  MIT License http://www.opensource.org/licenses/mit-license.php\n  Author Tobias Koppers @sokra\n*/\nmodule.exports = function (cssWithMappingToString) {\n  var list = [];\n\n  // return the list of modules as css string\n  list.toString = function toString() {\n    return this.map(function (item) {\n      var content = \"\";\n      var needLayer = typeof item[5] !== \"undefined\";\n      if (item[4]) {\n        content += \"@supports (\".concat(item[4], \") {\");\n      }\n      if (item[2]) {\n        content += \"@media \".concat(item[2], \" {\");\n      }\n      if (needLayer) {\n        content += \"@layer\".concat(item[5].length > 0 ? \" \".concat(item[5]) : \"\", \" {\");\n      }\n      content += cssWithMappingToString(item);\n      if (needLayer) {\n        content += \"}\";\n      }\n      if (item[2]) {\n        content += \"}\";\n      }\n      if (item[4]) {\n        content += \"}\";\n      }\n      return content;\n    }).join(\"\");\n  };\n\n  // import a list of modules into the list\n  list.i = function i(modules, media, dedupe, supports, layer) {\n    if (typeof modules === \"string\") {\n      modules = [[null, modules, undefined]];\n    }\n    var alreadyImportedModules = {};\n    if (dedupe) {\n      for (var k = 0; k < this.length; k++) {\n        var id = this[k][0];\n        if (id != null) {\n          alreadyImportedModules[id] = true;\n        }\n      }\n    }\n    for (var _k = 0; _k < modules.length; _k++) {\n      var item = [].concat(modules[_k]);\n      if (dedupe && alreadyImportedModules[item[0]]) {\n        continue;\n      }\n      if (typeof layer !== \"undefined\") {\n        if (typeof item[5] === \"undefined\") {\n          item[5] = layer;\n        } else {\n          item[1] = \"@layer\".concat(item[5].length > 0 ? \" \".concat(item[5]) : \"\", \" {\").concat(item[1], \"}\");\n          item[5] = layer;\n        }\n      }\n      if (media) {\n        if (!item[2]) {\n          item[2] = media;\n        } else {\n          item[1] = \"@media \".concat(item[2], \" {\").concat(item[1], \"}\");\n          item[2] = media;\n        }\n      }\n      if (supports) {\n        if (!item[4]) {\n          item[4] = \"\".concat(supports);\n        } else {\n          item[1] = \"@supports (\".concat(item[4], \") {\").concat(item[1], \"}\");\n          item[4] = supports;\n        }\n      }\n      list.push(item);\n    }\n  };\n  return list;\n};\n\n//# sourceURL=webpack://fv/./node_modules/css-loader/dist/runtime/api.js?");

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/noSourceMaps.js":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/noSourceMaps.js ***!
  \**************************************************************/
/***/ ((module) => {

eval("\n\nmodule.exports = function (i) {\n  return i[1];\n};\n\n//# sourceURL=webpack://fv/./node_modules/css-loader/dist/runtime/noSourceMaps.js?");

/***/ }),

/***/ "./src/css/style.css":
/*!***************************!*\
  !*** ./src/css/style.css ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\");\n/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/styleDomAPI.js */ \"./node_modules/style-loader/dist/runtime/styleDomAPI.js\");\n/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/insertBySelector.js */ \"./node_modules/style-loader/dist/runtime/insertBySelector.js\");\n/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ \"./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js\");\n/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/insertStyleElement.js */ \"./node_modules/style-loader/dist/runtime/insertStyleElement.js\");\n/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);\n/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../../node_modules/style-loader/dist/runtime/styleTagTransform.js */ \"./node_modules/style-loader/dist/runtime/styleTagTransform.js\");\n/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);\n/* harmony import */ var _node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../../node_modules/css-loader/dist/cjs.js!./style.css */ \"./node_modules/css-loader/dist/cjs.js!./src/css/style.css\");\n\n      \n      \n      \n      \n      \n      \n      \n      \n      \n\nvar options = {};\n\noptions.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());\noptions.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());\noptions.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, \"head\");\noptions.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());\noptions.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());\n\nvar update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__[\"default\"], options);\n\n\n\n\n       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__[\"default\"] && _node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__[\"default\"].locals ? _node_modules_css_loader_dist_cjs_js_style_css__WEBPACK_IMPORTED_MODULE_6__[\"default\"].locals : undefined);\n\n\n//# sourceURL=webpack://fv/./src/css/style.css?");

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {

eval("\n\nvar stylesInDOM = [];\nfunction getIndexByIdentifier(identifier) {\n  var result = -1;\n  for (var i = 0; i < stylesInDOM.length; i++) {\n    if (stylesInDOM[i].identifier === identifier) {\n      result = i;\n      break;\n    }\n  }\n  return result;\n}\nfunction modulesToDom(list, options) {\n  var idCountMap = {};\n  var identifiers = [];\n  for (var i = 0; i < list.length; i++) {\n    var item = list[i];\n    var id = options.base ? item[0] + options.base : item[0];\n    var count = idCountMap[id] || 0;\n    var identifier = \"\".concat(id, \" \").concat(count);\n    idCountMap[id] = count + 1;\n    var indexByIdentifier = getIndexByIdentifier(identifier);\n    var obj = {\n      css: item[1],\n      media: item[2],\n      sourceMap: item[3],\n      supports: item[4],\n      layer: item[5]\n    };\n    if (indexByIdentifier !== -1) {\n      stylesInDOM[indexByIdentifier].references++;\n      stylesInDOM[indexByIdentifier].updater(obj);\n    } else {\n      var updater = addElementStyle(obj, options);\n      options.byIndex = i;\n      stylesInDOM.splice(i, 0, {\n        identifier: identifier,\n        updater: updater,\n        references: 1\n      });\n    }\n    identifiers.push(identifier);\n  }\n  return identifiers;\n}\nfunction addElementStyle(obj, options) {\n  var api = options.domAPI(options);\n  api.update(obj);\n  var updater = function updater(newObj) {\n    if (newObj) {\n      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {\n        return;\n      }\n      api.update(obj = newObj);\n    } else {\n      api.remove();\n    }\n  };\n  return updater;\n}\nmodule.exports = function (list, options) {\n  options = options || {};\n  list = list || [];\n  var lastIdentifiers = modulesToDom(list, options);\n  return function update(newList) {\n    newList = newList || [];\n    for (var i = 0; i < lastIdentifiers.length; i++) {\n      var identifier = lastIdentifiers[i];\n      var index = getIndexByIdentifier(identifier);\n      stylesInDOM[index].references--;\n    }\n    var newLastIdentifiers = modulesToDom(newList, options);\n    for (var _i = 0; _i < lastIdentifiers.length; _i++) {\n      var _identifier = lastIdentifiers[_i];\n      var _index = getIndexByIdentifier(_identifier);\n      if (stylesInDOM[_index].references === 0) {\n        stylesInDOM[_index].updater();\n        stylesInDOM.splice(_index, 1);\n      }\n    }\n    lastIdentifiers = newLastIdentifiers;\n  };\n};\n\n//# sourceURL=webpack://fv/./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js?");

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {

eval("\n\nvar memo = {};\n\n/* istanbul ignore next  */\nfunction getTarget(target) {\n  if (typeof memo[target] === \"undefined\") {\n    var styleTarget = document.querySelector(target);\n\n    // Special case to return head of iframe instead of iframe itself\n    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {\n      try {\n        // This will throw an exception if access to iframe is blocked\n        // due to cross-origin restrictions\n        styleTarget = styleTarget.contentDocument.head;\n      } catch (e) {\n        // istanbul ignore next\n        styleTarget = null;\n      }\n    }\n    memo[target] = styleTarget;\n  }\n  return memo[target];\n}\n\n/* istanbul ignore next  */\nfunction insertBySelector(insert, style) {\n  var target = getTarget(insert);\n  if (!target) {\n    throw new Error(\"Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.\");\n  }\n  target.appendChild(style);\n}\nmodule.exports = insertBySelector;\n\n//# sourceURL=webpack://fv/./node_modules/style-loader/dist/runtime/insertBySelector.js?");

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {

eval("\n\n/* istanbul ignore next  */\nfunction insertStyleElement(options) {\n  var element = document.createElement(\"style\");\n  options.setAttributes(element, options.attributes);\n  options.insert(element, options.options);\n  return element;\n}\nmodule.exports = insertStyleElement;\n\n//# sourceURL=webpack://fv/./node_modules/style-loader/dist/runtime/insertStyleElement.js?");

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("\n\n/* istanbul ignore next  */\nfunction setAttributesWithoutAttributes(styleElement) {\n  var nonce =  true ? __webpack_require__.nc : 0;\n  if (nonce) {\n    styleElement.setAttribute(\"nonce\", nonce);\n  }\n}\nmodule.exports = setAttributesWithoutAttributes;\n\n//# sourceURL=webpack://fv/./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js?");

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {

eval("\n\n/* istanbul ignore next  */\nfunction apply(styleElement, options, obj) {\n  var css = \"\";\n  if (obj.supports) {\n    css += \"@supports (\".concat(obj.supports, \") {\");\n  }\n  if (obj.media) {\n    css += \"@media \".concat(obj.media, \" {\");\n  }\n  var needLayer = typeof obj.layer !== \"undefined\";\n  if (needLayer) {\n    css += \"@layer\".concat(obj.layer.length > 0 ? \" \".concat(obj.layer) : \"\", \" {\");\n  }\n  css += obj.css;\n  if (needLayer) {\n    css += \"}\";\n  }\n  if (obj.media) {\n    css += \"}\";\n  }\n  if (obj.supports) {\n    css += \"}\";\n  }\n  var sourceMap = obj.sourceMap;\n  if (sourceMap && typeof btoa !== \"undefined\") {\n    css += \"\\n/*# sourceMappingURL=data:application/json;base64,\".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), \" */\");\n  }\n\n  // For old IE\n  /* istanbul ignore if  */\n  options.styleTagTransform(css, styleElement, options.options);\n}\nfunction removeStyleElement(styleElement) {\n  // istanbul ignore if\n  if (styleElement.parentNode === null) {\n    return false;\n  }\n  styleElement.parentNode.removeChild(styleElement);\n}\n\n/* istanbul ignore next  */\nfunction domAPI(options) {\n  if (typeof document === \"undefined\") {\n    return {\n      update: function update() {},\n      remove: function remove() {}\n    };\n  }\n  var styleElement = options.insertStyleElement(options);\n  return {\n    update: function update(obj) {\n      apply(styleElement, options, obj);\n    },\n    remove: function remove() {\n      removeStyleElement(styleElement);\n    }\n  };\n}\nmodule.exports = domAPI;\n\n//# sourceURL=webpack://fv/./node_modules/style-loader/dist/runtime/styleDomAPI.js?");

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {

eval("\n\n/* istanbul ignore next  */\nfunction styleTagTransform(css, styleElement) {\n  if (styleElement.styleSheet) {\n    styleElement.styleSheet.cssText = css;\n  } else {\n    while (styleElement.firstChild) {\n      styleElement.removeChild(styleElement.firstChild);\n    }\n    styleElement.appendChild(document.createTextNode(css));\n  }\n}\nmodule.exports = styleTagTransform;\n\n//# sourceURL=webpack://fv/./node_modules/style-loader/dist/runtime/styleTagTransform.js?");

/***/ }),

/***/ "./src/js/formFunctions.js":
/*!*********************************!*\
  !*** ./src/js/formFunctions.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   _Initialize: () => (/* binding */ _Initialize),\n/* harmony export */   _InitializeForms: () => (/* binding */ _InitializeForms),\n/* harmony export */   checkForm: () => (/* binding */ checkForm),\n/* harmony export */   csrftoken: () => (/* binding */ csrftoken),\n/* harmony export */   fetchHandleForm: () => (/* binding */ fetchHandleForm)\n/* harmony export */ });\n// ########## Getting the csrf token for the fetch calls ##########\r\nfunction getCookie(name) {\r\n    let cookieValue = null;\r\n    if (document.cookie && document.cookie !== '') {\r\n        const cookies = document.cookie.split(';');\r\n        for (let i = 0; i < cookies.length; i++) {\r\n            const cookie = cookies[i].trim();\r\n            // Does this cookie string begin with the name we want?\r\n            if (cookie.substring(0, name.length + 1) === (name + '=')) {\r\n                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));\r\n                break;\r\n            }\r\n        }\r\n    }\r\n    return cookieValue;\r\n}\r\nconst csrftoken = getCookie('csrftoken');\r\n\r\n// ##### Fetch Calls #####\r\n// performs fetch call to view\r\nconst fetchHandleForm = async (form) => {\r\n    let formData = new FormData(form);\r\n    return await fetch(form.action, {\r\n        method: \"POST\",\r\n        credentials: \"same-origin\",\r\n        headers: {\r\n            // \"Accept\": \"m\",\r\n            // \"X-Requested-With\": \"XMLHttpRequest\",\r\n            \"X-CSRFToken\": csrftoken,\r\n        },\r\n        body: formData,\r\n    }).then(async (response) => {\r\n        return response.json();\r\n    });\r\n}\r\n// ***** Adding asterisks to labels of required inputs *****\r\nfunction addAsterisks(form) {\r\n    // gathering all inputs\r\n    let formGroups = document.querySelectorAll(`#${form.id} .form-group`);\r\n    let inputs = getRequiredFields(formGroups);\r\n\r\n    // adding the required-field class which will add the asterisk\r\n    for (let i = 0; i < inputs.length; i++) {\r\n        let label = document.querySelector(`label[for=${inputs[i].name}]`);\r\n        if (inputs[i].required) {\r\n            label.classList.add(\"required-field\");\r\n        }\r\n    }\r\n}\r\n\r\n// In-line validation on required fields\r\nfunction validateInputs(form) {\r\n    // gathering all inputs\r\n    let formGroups = document.querySelectorAll(`#${form.id} .form-group`);\r\n    let inputs = getRequiredFields(formGroups);\r\n\r\n    // adding listeners to each input for validation\r\n    for (let i = 0; i < inputs.length; i++) {\r\n        inputs[i].addEventListener(\"focusout\", () => {\r\n            if (inputs[i].value === \"\" || inputs[i].value === null) {\r\n                addError(inputs[i]);\r\n            } else {\r\n                removeError(inputs[i]);\r\n            }\r\n        });\r\n    }\r\n}\r\n// validateInputs();\r\n\r\n// check form function\r\nfunction checkForm(form) {\r\n    let errors = false;\r\n\r\n    // gathering all inputs\r\n    let formGroups = document.querySelectorAll(`#${form.id} .form-group`);\r\n    let inputs = getRequiredFields(formGroups);\r\n\r\n    // iterating through all required fields to check for invalidation\r\n    for (let i = 0; i < inputs.length; i++) {\r\n        let input = inputs[i];\r\n        if (input.value === \"\" || !input.value) {\r\n            addError(input);\r\n            errors = true;\r\n        }\r\n    }\r\n\r\n    return errors\r\n}\r\n\r\n// submit button validation check\r\nfunction submitValidation(form) {\r\n    form.form.addEventListener(\"submit\", (e) => {\r\n        // preventing default submission behavior\r\n        e.preventDefault();\r\n\r\n        // gathering all inputs\r\n        let f = e.target;\r\n        // let formGroups = document.querySelectorAll(`#${form.id} .form-group`);\r\n        // let inputs = getRequiredFields(formGroups);\r\n        // // let form = document.getElementById(\"form\") !== null ? document.getElementById(\"form\") : document.getElementById(\"userForm\");\r\n        let errors = checkForm(f);\r\n\r\n        // submitting the form if there aren't any errors\r\n        if (!errors) {\r\n            form.form.submit();\r\n        } else {\r\n            let invalidInputs = document.getElementsByClassName(\"validation-error\");\r\n            // scroll to the first invalid input\r\n            invalidInputs[0].parentElement.scrollIntoView();\r\n        }\r\n    });\r\n}\r\n// submitValidation();\r\n\r\n// adds an error to an input\r\nfunction addError(input) {\r\n    let inputParent = input.parentElement;\r\n    if (!inputParent.className.includes(\"form-group\")){\r\n        inputParent = input.parentElement.parentElement;\r\n    }\r\n    let errorAdded = inputParent.dataset.errorAdded;\r\n    inputParent.classList.add(\"validation-error\");\r\n    input.classList.add(\"error-input\")\r\n    if (errorAdded === \"false\" || !errorAdded) {\r\n        // creating the error message p\r\n        let eP = document.createElement(\"p\");\r\n        eP.setAttribute(\"class\", \"error-msg\");\r\n        eP.innerText = \"This input is required\";\r\n        inputParent.appendChild(eP);\r\n        inputParent.dataset.errorAdded = \"true\";\r\n    }\r\n}\r\n\r\n// removes the error from an input\r\nfunction removeError(input) {\r\n    let inputParent = input.parentElement;\r\n    if (!inputParent.className.includes(\"form-group\")){\r\n        inputParent = input.parentElement.parentElement;\r\n    }\r\n    let errorAdded = inputParent.dataset.errorAdded;\r\n    inputParent.classList.remove(\"validation-error\");\r\n    input.classList.remove(\"error-input\");\r\n    // removing the error message p\r\n    if (errorAdded === \"true\") {\r\n        inputParent.removeChild(inputParent.lastElementChild);\r\n        inputParent.dataset.errorAdded = \"false\";\r\n    }\r\n}\r\n\r\n// function to get all required input\r\nfunction getRequiredFields(formGroups) {\r\n    let nameList = [\"SELECT\", \"INPUT\", \"TEXTAREA\"];\r\n    let inputs = [];\r\n    // let formGroups = document.getElementsByClassName(\"form-group\");\r\n    for (let i = 0; i < formGroups.length; i++) {\r\n        let children = formGroups[i].children;\r\n        for (let j = 0; j < children.length; j++) {\r\n            if (children[j].tagName === \"DIV\"){\r\n                let grandChildren = children[j].children;\r\n                for (let a = 0; a < grandChildren.length; a++) {\r\n                    if (nameList.includes(grandChildren[a].tagName)) {\r\n                        if (grandChildren[a].required) {\r\n                            inputs.push(grandChildren[a]);\r\n                        }\r\n                    }\r\n                }\r\n            }\r\n            else{\r\n                if (nameList.includes(children[j].tagName)) {\r\n                    if (children[j].required) {\r\n                        inputs.push(children[j]);\r\n                    }\r\n                }\r\n            }\r\n        }\r\n    }\r\n    return inputs\r\n}\r\n\r\n// checks if the form will be ignored form validation.\r\nfunction getIgnored(form, ignoredClasses) {\r\n    let isIgnored = false;\r\n    let classes = form.classList;\r\n    if (ignoredClasses.length > 0) {\r\n        classes.forEach((_class) => {\r\n            if (ignoredClasses.includes(_class)) {\r\n                isIgnored = true;\r\n                return isIgnored;\r\n            }\r\n        });\r\n    }\r\n    return isIgnored\r\n}\r\n\r\n// Checks if the form will be validated.\r\nfunction isValidate(form, ignoredClasses) {\r\n    let enableValidate = true;\r\n    let classes = form.classList;\r\n    if (ignoredClasses.length > 0) {\r\n        classes.forEach((_class) => {\r\n            if (ignoredClasses.includes(_class)) {\r\n                enableValidate = false;\r\n                return enableValidate;\r\n            }\r\n        });\r\n    }\r\n    return enableValidate\r\n}\r\n\r\n// Confirms if a form will only validate the form on submit, only.\r\nfunction getValidateOnlyValidateOnSubmit(form, validateOnlyOnSubmit, enableValidation) {\r\n    let validateOnSubmit = false;\r\n    let trueFlags = [\"all\", \"__all__\", \"*\", \"true\"];\r\n    if (enableValidation) {\r\n        let classes = form.classList;\r\n        if (trueFlags.includes(validateOnlyOnSubmit[0])) {\r\n            validateOnSubmit = true;\r\n            return true;\r\n        }\r\n        else {\r\n            classes.forEach((_class) => {\r\n                if (validateOnlyOnSubmit.includes(_class)) {\r\n                    validateOnSubmit = true;\r\n                    return validateOnlyOnSubmit;\r\n                }\r\n            });\r\n        }\r\n    }\r\n    return validateOnSubmit;\r\n}\r\n\r\n// adds listener logic to the form\r\nfunction _Initialize(form={}){\r\n    if (!form.ignored || form.enableValidation) {\r\n        // add all listeners to each form\r\n        addAsterisks(form);\r\n        if (!form.validateOnlyOnSubmit) {\r\n            validateInputs(form);\r\n        }\r\n        if (!form.ignored) {\r\n            submitValidation(form);\r\n        }\r\n    }\r\n}\r\n\r\n// function to initialize forms into a json object\r\nfunction _InitializeForms(formNodes, ignoredFormClasses=[], ignoredValidationClasses=[], validateOnlyOnSubmit){\r\n    for (let i = 0; i < formNodes.length; i++) {\r\n        let currentForm = formNodes[i];\r\n        let ignored = getIgnored(currentForm, ignoredFormClasses);\r\n        let enableValidation = isValidate(currentForm, ignoredValidationClasses);\r\n        let validateOnSubmit = getValidateOnlyValidateOnSubmit(currentForm, validateOnlyOnSubmit, enableValidation);\r\n        let _form = {\r\n            id: currentForm.id,\r\n            form: currentForm,\r\n            ignored: ignored,\r\n            enableValidation: enableValidation,\r\n            validateOnlyOnSubmit: validateOnSubmit,\r\n        }\r\n\r\n        // adding form functionality\r\n        _Initialize(_form);\r\n    }\r\n}\n\n//# sourceURL=webpack://fv/./src/js/formFunctions.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/nonce */
/******/ 	(() => {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	__webpack_require__("./src/css/style.css");
/******/ 	var __webpack_exports__ = __webpack_require__("./src/js/formFunctions.js");
/******/ 	
/******/ 	return __webpack_exports__;
/******/ })()
;
});