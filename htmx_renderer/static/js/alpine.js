document.addEventListener('alpine:init', () => {
  Alpine.data('xForeignKey', (searchMethod, baseUrl, selected, baseHtmxUrl, isFilter, choices) => ({
    searchMethod,
    baseUrl,
    selected,
    baseHtmxUrl,
    isFilter,
    choices,
    open: false,
    toggle(){
      this.open = !this.open;
      if (this.open && this.searchMethod == 'backend' && this.choices.length < 2) {
        this.fetch().then((data) => {
          this.choices = this.choices.concat(data.filter((item) => item.key != this.selected));
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
      const url = `${this.baseUrl}&search=${search}`;
      const response = await fetch(url);
      const results = await response.json();
      return results.results.map((item) => { return {key: '' + item.id, label: item.__str__}; });
    },
    async getFilteredChoices() {
      if (this.search == '') {
        return this.choices;
      }
      if (this.searchMethod == 'backend') {
        const rv = await this.fetch(this.search);
        const knownKeys = this.choices.map((item) => item.key);
        this.choices = this.choices.concat(rv.filter((item) => !knownKeys.includes(item.key)));
        return rv;
      } else {
        return this.choices.filter((item) => {
          return item.label.toLowerCase().includes(this.search.toLowerCase());
        });
      }
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
            window.history.pushState({}, 'UrlHtmx' + value);
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
        if (results.next) {
          let gottenPage = /page=(\d+)/.exec(results.next);
          if (gottenPage && gottenPage[1] - 1 > this.lastPage) {
            this.lastPage = gottenPage[1] - 1;
          }
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
