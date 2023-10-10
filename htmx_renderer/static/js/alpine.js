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
  }))
});
