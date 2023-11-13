document.addEventListener('alpine:init', () => {
  Alpine.data('xDuration', (time) => ({
    time,
    
    get fromValue() {
      let from = this.time;
      let days = 0;
      const days_part = this.time.split(" ");
      if (days_part.length > 1) {
        days = parseInt(days_part[0], 10);
        from = days_part[1];
      }
      const time_parts = from.split(":");
      const hours = parseInt(time_parts[0]) + days * 24;
      const minutes = parseInt(time_parts[1]);

      return ("" + hours).padStart(2, 0) + ":" + ("" + minutes).padStart(2, 0);
    },
    toVal(e) {
      entered = e.target.value;
      let hours = 0;
      let minutes = 0;

      let entered_parts = entered.split(":");
 
      if (entered_parts.length > 2) {
        entered_parts = entered_parts.slice(-2);
      }

      if (entered_parts.length == 2) {
        hours = parseInt(entered_parts[0], 10);
      }
      if (isNaN(hours)) {
        hours = 0;
      }

      const minutes_part = entered_parts[entered_parts.length - 1];
      minutes = parseInt(minutes_part, 10);
      if (isNaN(minutes)) {
        minutes = 0;
      }

      hours += Math.floor(minutes / 60);
      minutes = minutes % 60;

      this.time = ("" + hours).padStart(2, 0) + ":" + ("" + minutes).padStart(2, 0) + ":00";
    },
  })),
  Alpine.data('xManytomanyLists', (searchMethod, selected, baseUrl, choices) => ({
    searchMethod,
    selected,
    baseUrl,
    choices,
    search: '',
    selectedAvailable: [],
    selectedChosen: [],
    lastPage: 0,
    resultsCount: -1,
    checkedAll: false,
    get canLoadMore() {
      return this.search == '' && this.resultsCount > this.choices.length;
    },
    async fetch(search='') {
      let url = `${this.baseUrl}`
      if (search == ''){
        url += `&page=${this.lastPage +1}`;
      } else {
        url += `&search=${search}`;
      }
      const response = await fetch(url);
      const results = await response.json();
      if (search=='' && this.resultsCount <= 0) {
        this.resultsCount = results.count;
      }
      if (search == '') {
        if (results.next)  {
          let gottenPage = /page=(\d+)/.exec(results.next);
          if (gottenPage && gottenPage[1] -1 > this.lastPage) {
            this.lastPage = gottenPage[1] - 1;
          }
        } else {
          this.lastPage = 1;
        }
      }
      return results.results.map((item) => ({key: '' + item.id, label: item.__str__}));
    },
    mergeChoicesWith(data) {
      const knownKeys = this.choices.map((item) => item.key) ;
      this.choices = this.choices.concat(
        data.filter((item) => !knownKeys.includes(item.key))
      );
    },
    async fetchAndMerge(search='') {
      const rv = await this.fetch(search);
      this.mergeChoicesWith(rv);
      return this.unSelectedChoices;
    },
    async getFilteredChoices() {
      const origChoices = this.unSelectedChoices;
      if (this.searchMethod == 'backend') {
        if (this.resultsCount < 0) {
          return this.fetchAndMerge(this.search);
        } else if (this.search != '') {
          const rv = await this.fetch(this.search);
          this.mergeChoicesWith(rv);
          return rv.filter((item) => !this.selected.includes(item.key));
        } else {
          return origChoices;
        }
      } else {
        if (this.search == '') {
          return origChoices;
        }
        return origChoices.filter((item) => item.label.toLowerCase().includes(this.search.toLowerCase()));
      }
    },
    get unSelectedChoices() {
      return this.choices.filter((item) => !this.selected.includes(item.key));
    },
    get selectedChoices() {
      return this.choices.filter((item) => this.selected.includes(item.key));
    },
    selectFromList(key, list) {
      if (this[list].indexOf(key) == -1) {
        this[list].push(key);
      } else {
        this[list] = this[list].filter((item) => item != key);
      }
    },
    isSelectedInList(key, list) {
      return this[list].indexOf(key) != -1;
    },
    select() {
      this.selectedAvailable.map((key) => {
        if (!this.selected.includes(key)) {
          this.selected.push(key);
        }
      });
      this.selectedAvailable = [];
    },
    unSelect() {
      this.selected = this.selected.filter((item) => !this.selectedChosen.includes(item));
      this.selectedChosen = [];
    },
    async selectAll() {
      const toSelect = await this.getFilteredChoices();
      this.selected = this.selected.concat(toSelect.map((item) => item.key));

      this.selectedAvailable = [];
    },
    unSelectAll() {
      this.selected = [];
      this.selectedChosen = [];
    },
    
  }));
  Alpine.data('xForeignKey', (searchMethod, baseUrl, selected, baseHtmxUrl, isFilter, choices, initialChoicesLength) => ({
    searchMethod,
    baseUrl,
    selected,
    baseHtmxUrl,
    isFilter,
    choices,
    initialChoicesLength,
    resultsCount: 0,
    lastPage: 0,
    open: false,
    toggle(){
      this.open = !this.open;
      if (this.open && this.searchMethod == 'backend' && this.choices.length <= this.initialChoicesLength) {
        this.fetch().then((data) => {
          this.mergeChoicesWith(data);
        });
      }
    },
    select(value){
      this.open=false;
      if (value == this.selected) {
        return;
      }
      if (value != '') {
        this.selected=value;
      } else {
        this.selected=null;
      }
      if (document.querySelector('#data-table-content')) {
        htmx.ajax(
          'GET',
           this.baseHtmxUrl + value,
          {
            target: '#data-table-content',
            swap: 'outerHTML swap:.3s',
                
          }
        ).then(() => {
          if (this.isFilter) {
            window.history.pushState({}, '', this.baseHtmxUrl + value);
          }
        });
      }
    },
    search: '',
    get selectedLabel() {
      const filtered = this.choices.filter((item) => { return item.key == this.selected; });
      if (filtered.length == 0) {
        return '--';
      }
      return filtered[0].label;
    },
    async fetch(search='') {
      let url = `${this.baseUrl}`
      if (search == '') {
        url += `&page=${this.lastPage + 1}`;
      } else {
        url += `&search=${search}`;
      }
      const response = await fetch(url);
      const results = await response.json();
      if (search=='' && this.resultsCount == 0) {
        this.resultsCount = results.count;
      }
      if (results.next && search=='') {
        let gottenPage = /page=(\d+)/.exec(results.next);
        if (gottenPage && gottenPage[1] -1 > this.lastPage) {
          this.lastPage = gottenPage[1] -1;
        }
      }
      return results.results.map((item) => { return {key: '' + item.id, label: item.__str__}; });
    },
    mergeChoicesWith(data){
      const knownKeys = this.choices.map((item) => item.key);
      this.choices = this.choices.concat(data.filter((item) => !knownKeys.includes(item.key)));
    },
    async getFilteredChoices() {
      if (this.search == '') {
        return this.choices;
      }
      if (this.searchMethod == 'backend') {
        const rv = await this.fetch(this.search);
        const knownKeys = this.choices.map((item) => item.key);
        this.mergeChoicesWith(rv);
        return rv;
      } else {
        return this.choices.filter((item) => {
          return item.label.toLowerCase().includes(this.search.toLowerCase());
        });
      }
    },
    get hasMoreResults() {
      return this.choices.length < this.resultsCount && this.search == '';
    },
    loadMore() {
      this.fetch().then((data) => {
        this.mergeChoicesWith(data);
      });
    },
  }));
  Alpine.data('xManytomany', (searchMethod, selected, baseUrl, baseHtmxUrl, isFilter, choices, initialChoicesLength) => ({
    searchMethod,
    selected,
    baseUrl,
    baseHtmxUrl,
    isFilter,
    choices,
    initialChoicesLength,
    resultsCount: 0,
    lastPage: 0,
    open: false,
    toggle(){
      this.open = !this.open;
      console.log(this.open, this.searchMethod == 'backend', this.choices.length, this.initialChoicesLength);
      if (this.open && this.searchMethod == 'backend' && this.choices.length <= this.initialChoicesLength) {
        this.fetch().then((data) => {
          this.mergeChoicesWith(data);
        });
      } 
    },
    isSelected(value) {
      return this.selected.indexOf(value) != -1;
    },
    select(value){
      if (this.isSelected(value)) {
        this.selected = this.selected.filter((item) => item != value);
      } else {
          this.selected.push(value);
      }
      if (document.querySelector('#data-table-content')) {
       htmx.ajax(
         'GET',
         this.baseHtmxUrl + value,
        {
          target: '#data-table-content',
          swap: 'outerHTML swap:.3s',
          }
         ).then(() => {
           if (this.isFilter) {
            window.history.pushState({},'', this.baseHtmxUrlHtmx + value);
           }
        });
      }
    },
    search: '',
    async fetch(search=''){
      let url = `${this.baseUrl}`
      if (search == '') {
        url += `&page=${this.lastPage + 1}`;
      } else {
        url += `&search=${search}`;
      }
      const response = await fetch(url);
      const results = await response.json();
      if (search=='' && this.resultsCount == 0) {
        this.resultsCount =results.count;
      }
      if (results.next && search=='') {
        let gottenPage = /page=(\d+)/.exec(results.next);
        if (gottenPage && gottenPage[1] - 1 > this.lastPage) {
         this.lastPage = gottenPage[1] - 1;
        }
      }
      return results.results.map((item) => {return { key: '' + item.id, label: item.__str__ }; });
    },
    mergeChoicesWith(data) {
      const knownKeys = this.choices.map((item) => item.key);
      this.choices = this.choices.concat(data.filter((item) => !knownKeys.includes(item.key)));
    },
    async getFilteredChoices() {
      console.log('searching', this.search)
      if (this.search == '') {
         return this.choices;
      }
      if (this.searchMethod == 'backend') {
        const rv = await this.fetch(this.search);
        this.mergeChoicesWith(rv);
        return rv
      } else {
        return this.choices.filter((item) => {
          return item.label.toLowerCase.includes(this.search.toLowerCase());
        });
      }
    },
    get hasMoreResults() {
      return this.choices.length < this.resultsCount && this.search == '';
    },
    loadMore() {
      this.fetch().then((data) => {
        this.mergeChoicesWith(data);
      });
    },
  }));
});
