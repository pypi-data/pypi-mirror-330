"use strict";
(self["webpackChunkmtd_mobile_ui"] = self["webpackChunkmtd_mobile_ui"] || []).push([["packages_mtd-mobile-ui_src_app_flashcards_flashcards_module_ts"],{

/***/ 8125:
/*!********************************************************************************!*\
  !*** ./packages/mtd-mobile-ui/src/app/flashcards/flashcards-routing.module.ts ***!
  \********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FlashcardsPageRoutingModule: () => (/* binding */ FlashcardsPageRoutingModule)
/* harmony export */ });
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ 7947);
/* harmony import */ var _flashcards_page__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./flashcards.page */ 4813);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);




const routes = [{
  path: '',
  component: _flashcards_page__WEBPACK_IMPORTED_MODULE_0__.FlashcardsPage
}];
class FlashcardsPageRoutingModule {}
FlashcardsPageRoutingModule.ɵfac = function FlashcardsPageRoutingModule_Factory(t) {
  return new (t || FlashcardsPageRoutingModule)();
};
FlashcardsPageRoutingModule.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineNgModule"]({
  type: FlashcardsPageRoutingModule
});
FlashcardsPageRoutingModule.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjector"]({
  imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule.forChild(routes), _angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule]
});
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsetNgModuleScope"](FlashcardsPageRoutingModule, {
    imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule],
    exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule]
  });
})();

/***/ }),

/***/ 3721:
/*!************************************************************************!*\
  !*** ./packages/mtd-mobile-ui/src/app/flashcards/flashcards.module.ts ***!
  \************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FlashcardsPageModule: () => (/* binding */ FlashcardsPageModule)
/* harmony export */ });
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @ionic/angular */ 4210);
/* harmony import */ var _flashcards_routing_module__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./flashcards-routing.module */ 8125);
/* harmony import */ var _flashcards_page__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./flashcards.page */ 4813);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 1699);






class FlashcardsPageModule {}
FlashcardsPageModule.ɵfac = function FlashcardsPageModule_Factory(t) {
  return new (t || FlashcardsPageModule)();
};
FlashcardsPageModule.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineNgModule"]({
  type: FlashcardsPageModule
});
FlashcardsPageModule.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineInjector"]({
  imports: [_angular_common__WEBPACK_IMPORTED_MODULE_3__.CommonModule, _angular_forms__WEBPACK_IMPORTED_MODULE_4__.FormsModule, _ionic_angular__WEBPACK_IMPORTED_MODULE_5__.IonicModule, _flashcards_routing_module__WEBPACK_IMPORTED_MODULE_0__.FlashcardsPageRoutingModule]
});
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵsetNgModuleScope"](FlashcardsPageModule, {
    declarations: [_flashcards_page__WEBPACK_IMPORTED_MODULE_1__.FlashcardsPage],
    imports: [_angular_common__WEBPACK_IMPORTED_MODULE_3__.CommonModule, _angular_forms__WEBPACK_IMPORTED_MODULE_4__.FormsModule, _ionic_angular__WEBPACK_IMPORTED_MODULE_5__.IonicModule, _flashcards_routing_module__WEBPACK_IMPORTED_MODULE_0__.FlashcardsPageRoutingModule]
  });
})();

/***/ }),

/***/ 4813:
/*!**********************************************************************!*\
  !*** ./packages/mtd-mobile-ui/src/app/flashcards/flashcards.page.ts ***!
  \**********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FlashcardsPage: () => (/* binding */ FlashcardsPage)
/* harmony export */ });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @ionic/angular */ 4210);


class FlashcardsPage {
  constructor() {}
  ngOnInit() {}
}
FlashcardsPage.ɵfac = function FlashcardsPage_Factory(t) {
  return new (t || FlashcardsPage)();
};
FlashcardsPage.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({
  type: FlashcardsPage,
  selectors: [["mtd-flashcards"]],
  decls: 11,
  vars: 2,
  consts: [[3, "translucent"], ["slot", "start"], [3, "fullscreen"], ["collapse", "condense"], ["size", "large"]],
  template: function FlashcardsPage_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "ion-header", 0)(1, "ion-toolbar")(2, "ion-buttons", 1);
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "ion-menu-button");
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "ion-title");
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](5, "Flashcards");
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](6, "ion-content", 2)(7, "ion-header", 3)(8, "ion-toolbar")(9, "ion-title", 4);
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](10, "Flashcards");
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]()()()();
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("translucent", true);
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵadvance"](6);
      _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵproperty"]("fullscreen", true);
    }
  },
  dependencies: [_ionic_angular__WEBPACK_IMPORTED_MODULE_1__.IonButtons, _ionic_angular__WEBPACK_IMPORTED_MODULE_1__.IonContent, _ionic_angular__WEBPACK_IMPORTED_MODULE_1__.IonHeader, _ionic_angular__WEBPACK_IMPORTED_MODULE_1__.IonMenuButton, _ionic_angular__WEBPACK_IMPORTED_MODULE_1__.IonTitle, _ionic_angular__WEBPACK_IMPORTED_MODULE_1__.IonToolbar],
  styles: ["/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJmbGFzaGNhcmRzLnBhZ2UuY3NzIn0= */\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3BhY2thZ2VzL210ZC1tb2JpbGUtdWkvc3JjL2FwcC9mbGFzaGNhcmRzL2ZsYXNoY2FyZHMucGFnZS5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUNBLGdLQUFnSyIsInNvdXJjZVJvb3QiOiIifQ== */"]
});

/***/ })

}]);
//# sourceMappingURL=packages_mtd-mobile-ui_src_app_flashcards_flashcards_module_ts.js.map