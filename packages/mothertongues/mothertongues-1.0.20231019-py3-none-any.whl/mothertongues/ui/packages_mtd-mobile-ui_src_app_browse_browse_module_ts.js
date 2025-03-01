"use strict";
(self["webpackChunkmtd_mobile_ui"] = self["webpackChunkmtd_mobile_ui"] || []).push([["packages_mtd-mobile-ui_src_app_browse_browse_module_ts"],{

/***/ 6822:
/*!************************************************************************!*\
  !*** ./packages/mtd-mobile-ui/src/app/browse/browse-routing.module.ts ***!
  \************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BrowsePageRoutingModule: () => (/* binding */ BrowsePageRoutingModule)
/* harmony export */ });
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ 7947);
/* harmony import */ var _browse_page__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./browse.page */ 1407);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ 1699);




const routes = [{
  path: '',
  component: _browse_page__WEBPACK_IMPORTED_MODULE_0__.BrowsePage
}];
class BrowsePageRoutingModule {}
BrowsePageRoutingModule.ɵfac = function BrowsePageRoutingModule_Factory(t) {
  return new (t || BrowsePageRoutingModule)();
};
BrowsePageRoutingModule.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineNgModule"]({
  type: BrowsePageRoutingModule
});
BrowsePageRoutingModule.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjector"]({
  imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule.forChild(routes), _angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule]
});
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsetNgModuleScope"](BrowsePageRoutingModule, {
    imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule],
    exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__.RouterModule]
  });
})();

/***/ }),

/***/ 8830:
/*!****************************************************************!*\
  !*** ./packages/mtd-mobile-ui/src/app/browse/browse.module.ts ***!
  \****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BrowsePageModule: () => (/* binding */ BrowsePageModule)
/* harmony export */ });
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @ionic/angular */ 4210);
/* harmony import */ var _browse_routing_module__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./browse-routing.module */ 6822);
/* harmony import */ var _browse_page__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./browse.page */ 1407);
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../shared/shared.module */ 4515);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ 1699);







class BrowsePageModule {}
BrowsePageModule.ɵfac = function BrowsePageModule_Factory(t) {
  return new (t || BrowsePageModule)();
};
BrowsePageModule.ɵmod = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdefineNgModule"]({
  type: BrowsePageModule
});
BrowsePageModule.ɵinj = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵdefineInjector"]({
  imports: [_angular_common__WEBPACK_IMPORTED_MODULE_4__.CommonModule, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.FormsModule, _ionic_angular__WEBPACK_IMPORTED_MODULE_6__.IonicModule, _browse_routing_module__WEBPACK_IMPORTED_MODULE_0__.BrowsePageRoutingModule, _shared_shared_module__WEBPACK_IMPORTED_MODULE_2__.SharedModule]
});
(function () {
  (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_3__["ɵɵsetNgModuleScope"](BrowsePageModule, {
    declarations: [_browse_page__WEBPACK_IMPORTED_MODULE_1__.BrowsePage],
    imports: [_angular_common__WEBPACK_IMPORTED_MODULE_4__.CommonModule, _angular_forms__WEBPACK_IMPORTED_MODULE_5__.FormsModule, _ionic_angular__WEBPACK_IMPORTED_MODULE_6__.IonicModule, _browse_routing_module__WEBPACK_IMPORTED_MODULE_0__.BrowsePageRoutingModule, _shared_shared_module__WEBPACK_IMPORTED_MODULE_2__.SharedModule]
  });
})();

/***/ }),

/***/ 1407:
/*!**************************************************************!*\
  !*** ./packages/mtd-mobile-ui/src/app/browse/browse.page.ts ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BrowsePage: () => (/* binding */ BrowsePage)
/* harmony export */ });
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../data.service */ 8564);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ 8071);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ 3839);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs */ 9736);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ 1699);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/common */ 6575);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/forms */ 8849);
/* harmony import */ var _ionic_angular__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @ionic/angular */ 4210);
/* harmony import */ var _shared_entry_list_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../shared/entry-list.component */ 8044);








function BrowsePage_ion_select_option_14_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "ion-select-option");
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const category_r4 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtextInterpolate"](category_r4);
  }
}
function BrowsePage_ion_item_15_ion_select_option_2_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "ion-select-option");
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const letter_r6 = ctx.$implicit;
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtextInterpolate"](letter_r6);
  }
}
function BrowsePage_ion_item_15_Template(rf, ctx) {
  if (rf & 1) {
    const _r8 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵgetCurrentView"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "ion-item")(1, "ion-select", 15);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ionChange", function BrowsePage_ion_item_15_Template_ion_select_ionChange_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r8);
      const ctx_r7 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r7.handleLetterChange($event));
    })("ngModelChange", function BrowsePage_ion_item_15_Template_ion_select_ngModelChange_1_listener($event) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r8);
      const ctx_r9 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r9.selectedLetter = $event);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](2, BrowsePage_ion_item_15_ion_select_option_2_Template, 2, 1, "ion-select-option", 6);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](3, "ion-toast", 16);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("didDismiss", function BrowsePage_ion_item_15_Template_ion_toast_didDismiss_3_listener() {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵrestoreView"](_r8);
      const ctx_r10 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
      return _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵresetView"](ctx_r10.letterNotFound = false);
    });
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
  }
  if (rf & 2) {
    const ctx_r1 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngModel", ctx_r1.selectedLetter);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngForOf", ctx_r1.displayLetters);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("isOpen", ctx_r1.letterNotFound)("duration", 5000);
  }
}
function BrowsePage_div_16_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "div", 17);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](1, "mtd-entry-list", 18);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const currentTen_r11 = ctx.ngIf;
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("entries", currentTen_r11);
  }
}
function BrowsePage_div_23_ion_title_1_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "ion-title");
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipe"](2, "async");
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const currentStart_r12 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]().ngIf;
    const ctx_r13 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵnextContext"]();
    let tmp_0_0;
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtextInterpolate3"]("Viewing ", currentStart_r12.start + 1, " to ", currentStart_r12.start + 10, " of ", (tmp_0_0 = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipeBind1"](2, 3, ctx_r13.$currentEntries)) == null ? null : tmp_0_0.length, " Dictionary Entries");
  }
}
function BrowsePage_div_23_Template(rf, ctx) {
  if (rf & 1) {
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "div", 19);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](1, BrowsePage_div_23_ion_title_1_Template, 3, 5, "ion-title", 7);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
  }
  if (rf & 2) {
    const currentStart_r12 = ctx.ngIf;
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
    _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", currentStart_r12.start !== null);
  }
}
const _c0 = function (a0) {
  return {
    start: a0
  };
};
class BrowsePage {
  constructor(dataService) {
    this.dataService = dataService;
    this.displayLetters = [];
    this.$currentEntries = new rxjs__WEBPACK_IMPORTED_MODULE_3__.BehaviorSubject([]);
    this.$currentIndexStart = new rxjs__WEBPACK_IMPORTED_MODULE_3__.BehaviorSubject(0);
    this.$manualTrigger = new rxjs__WEBPACK_IMPORTED_MODULE_3__.BehaviorSubject(null);
    // Emit a combination of the start index and current entries any time either of them changes
    this.currentTen$ = (0,rxjs__WEBPACK_IMPORTED_MODULE_4__.combineLatest)([this.$currentIndexStart, this.$currentEntries, this.$manualTrigger]).pipe((0,rxjs__WEBPACK_IMPORTED_MODULE_5__.map)(([start, entries, _]) => entries.slice(start, start + 10)));
    this.currentLetter$ = this.currentTen$.pipe((0,rxjs__WEBPACK_IMPORTED_MODULE_5__.map)(entries => {
      if (entries && this.$config.value?.alphabet) {
        const firstNonOOVIndex = entries[0].sorting_form.filter(x => x < 10000)[0];
        return this.$config.value?.alphabet[firstNonOOVIndex];
      } else {
        return '';
      }
    }));
    this.categories = [];
    this.selectedLetter = '';
    this.letterNotFound = false;
  }
  ngOnInit() {
    this.$config = this.dataService.$config;
    this.$dataHash = this.dataService.$entriesHash;
    this.dataService.$categories.subscribe(categories => this.categories = categories);
    this.dataService.$categorizedEntries.subscribe(entries => {
      if (entries['All'] !== undefined && entries['All'].length > 0) {
        this.$currentEntries.next(entries['All']);
      }
    });
    this.currentLetter$.subscribe(letter => this.selectedLetter = letter);
    this.$config.subscribe(config => {
      if (config) {
        if (Array.isArray(config.alphabet)) {
          this.displayLetters = config.alphabet;
        } else {
          this.displayLetters = [...config.alphabet];
        }
      }
    });
  }
  handleLetterChange(letterEvent) {
    this.letterNotFound = false;
    const letterElement = letterEvent?.currentTarget;
    let found = false;
    for (const entry of this.$currentEntries.value) {
      if (entry.word.startsWith(letterElement.value)) {
        this.$currentIndexStart.next(this.$currentEntries.value.indexOf(entry));
        found = true;
        break;
      }
    }
    if (!found) {
      this.letterNotFound = true;
    }
  }
  handleCategoryChange(categoryEvent) {
    const categoryElement = categoryEvent?.currentTarget;
    this.$currentEntries.next(this.dataService.$categorizedEntries.value[categoryElement.value]);
    this.$currentIndexStart.next(0);
  }
  goBack() {
    this.$currentIndexStart.next(Math.max(0, this.$currentIndexStart.value - 10));
  }
  goForward() {
    this.$currentIndexStart.next(Math.min(this.$currentEntries.value.length - 10, this.$currentIndexStart.value + 10));
  }
}
BrowsePage.ɵfac = function BrowsePage_Factory(t) {
  return new (t || BrowsePage)(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdirectiveInject"](_data_service__WEBPACK_IMPORTED_MODULE_0__.DataService));
};
BrowsePage.ɵcmp = /*@__PURE__*/_angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineComponent"]({
  type: BrowsePage,
  selectors: [["mtd-browse"]],
  decls: 28,
  vars: 12,
  consts: [[3, "translucent"], ["slot", "start"], [3, "fullscreen"], ["collapse", "condense"], ["size", "large"], ["label", "Select a Category", "placeholder", "All", 3, "ionChange"], [4, "ngFor", "ngForOf"], [4, "ngIf"], ["class", "entry-container", 4, "ngIf"], ["slot", "start", 1, "bar-buttons", "bar-buttons-ios"], [3, "click"], ["slot", "icon-only", "name", "chevron-back-outline", 1, "scroll"], ["class", "browse-info", 4, "ngIf"], ["slot", "end", 1, "bar-buttons", "bar-buttons-ios"], ["slot", "icon-only", "name", "chevron-forward-outline", 1, "scroll"], ["label", "Current Letter", 3, "ngModel", "ionChange", "ngModelChange"], ["message", "Sorry, it doesn't look like there are any words that start with that letter", 3, "isOpen", "duration", "didDismiss"], [1, "entry-container"], [3, "entries"], [1, "browse-info"]],
  template: function BrowsePage_Template(rf, ctx) {
    if (rf & 1) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](0, "ion-header", 0)(1, "ion-toolbar")(2, "ion-buttons", 1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](3, "ion-menu-button");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](4, "ion-title");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](5, "Browse");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](6, "ion-content", 2)(7, "ion-header", 3)(8, "ion-toolbar")(9, "ion-title", 4);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtext"](10, "browse");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](11, "ion-list")(12, "ion-item")(13, "ion-select", 5);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("ionChange", function BrowsePage_Template_ion_select_ionChange_13_listener($event) {
        return ctx.handleCategoryChange($event);
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](14, BrowsePage_ion_select_option_14_Template, 2, 1, "ion-select-option", 6);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](15, BrowsePage_ion_item_15_Template, 4, 4, "ion-item", 7);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](16, BrowsePage_div_16_Template, 2, 1, "div", 8);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipe"](17, "async");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](18, "ion-footer")(19, "ion-toolbar")(20, "ion-buttons", 9)(21, "ion-button", 10);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("click", function BrowsePage_Template_ion_button_click_21_listener() {
        return ctx.goBack();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](22, "ion-icon", 11);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()();
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵtemplate"](23, BrowsePage_div_23_Template, 2, 1, "div", 12);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipe"](24, "async");
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementStart"](25, "ion-buttons", 13)(26, "ion-button", 10);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵlistener"]("click", function BrowsePage_Template_ion_button_click_26_listener() {
        return ctx.goForward();
      });
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelement"](27, "ion-icon", 14);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵelementEnd"]()()()();
    }
    if (rf & 2) {
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("translucent", true);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](6);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("fullscreen", true);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](8);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngForOf", ctx.categories);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", ctx.displayLetters);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](1);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipeBind1"](17, 6, ctx.currentTen$));
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵadvance"](7);
      _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵproperty"]("ngIf", _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpureFunction1"](10, _c0, _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵpipeBind1"](24, 8, ctx.$currentIndexStart)));
    }
  },
  dependencies: [_angular_common__WEBPACK_IMPORTED_MODULE_6__.NgForOf, _angular_common__WEBPACK_IMPORTED_MODULE_6__.NgIf, _angular_forms__WEBPACK_IMPORTED_MODULE_7__.NgControlStatus, _angular_forms__WEBPACK_IMPORTED_MODULE_7__.NgModel, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonButton, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonButtons, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonContent, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonFooter, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonHeader, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonIcon, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonItem, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonList, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonMenuButton, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonSelect, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonSelectOption, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonTitle, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonToast, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.IonToolbar, _ionic_angular__WEBPACK_IMPORTED_MODULE_8__.SelectValueAccessor, _shared_entry_list_component__WEBPACK_IMPORTED_MODULE_1__.EntryListComponent, _angular_common__WEBPACK_IMPORTED_MODULE_6__.AsyncPipe],
  styles: [".browse-info[_ngcontent-%COMP%] {\n  margin: 0 auto;\n  text-align: center;\n}\n\n@media only screen and (max-width: 600px) {\n  .browse-info[_ngcontent-%COMP%] {\n    display: none;\n  }\n}\n\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbImJyb3dzZS5wYWdlLmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGNBQWM7RUFDZCxrQkFBa0I7QUFDcEI7O0FBRUE7RUFDRTtJQUNFLGFBQWE7RUFDZjtBQUNGIiwiZmlsZSI6ImJyb3dzZS5wYWdlLmNzcyIsInNvdXJjZXNDb250ZW50IjpbIi5icm93c2UtaW5mbyB7XG4gIG1hcmdpbjogMCBhdXRvO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG59XG5cbkBtZWRpYSBvbmx5IHNjcmVlbiBhbmQgKG1heC13aWR0aDogNjAwcHgpIHtcbiAgLmJyb3dzZS1pbmZvIHtcbiAgICBkaXNwbGF5OiBub25lO1xuICB9XG59XG4iXX0= */\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8uL3BhY2thZ2VzL210ZC1tb2JpbGUtdWkvc3JjL2FwcC9icm93c2UvYnJvd3NlLnBhZ2UuY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsY0FBYztFQUNkLGtCQUFrQjtBQUNwQjs7QUFFQTtFQUNFO0lBQ0UsYUFBYTtFQUNmO0FBQ0Y7O0FBRUEsZ2ZBQWdmIiwic291cmNlc0NvbnRlbnQiOlsiLmJyb3dzZS1pbmZvIHtcbiAgbWFyZ2luOiAwIGF1dG87XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbn1cblxuQG1lZGlhIG9ubHkgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA2MDBweCkge1xuICAuYnJvd3NlLWluZm8ge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0= */"]
});

/***/ })

}]);
//# sourceMappingURL=packages_mtd-mobile-ui_src_app_browse_browse_module_ts.js.map