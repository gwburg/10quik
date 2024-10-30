import React from 'react';
//import { Autosuggest, AutosuggestHighlightMatch } from 'react-autosuggest';
import Autosuggest from 'react-autosuggest';
import AutosuggestHighlightMatch from 'autosuggest-highlight/match';
import AutosuggestHighlightParse from 'autosuggest-highlight/parse';
import './searchbar.css';

export default class SearchBar extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      value: '',
      suggestions: [],
      companies: [],
    };
    this.getCompanies();
  }

  getCompanies() {
    let headers = new Headers({
      "Content-Type": "application/json",
    });
    fetch(/*http://localhost:5000*/"/api/companies", {
      method: "GET",
      headers: headers,
    }).then(res => {
      return res.json()
    }).then(res => {
      this.setState({companies: res["companies"],});
    }).catch(error => {
      console.error('Error:', error);
    });
  }

  renderSuggestion = (suggestion, { query }) => {
    const companyString = suggestion.title.concat(" (", suggestion.ticker, ")");
    const matches = AutosuggestHighlightMatch(companyString, query);
    const parts = AutosuggestHighlightParse(companyString, matches);

    return (
      <span>
	{parts.map((part, index) => {
	  const className = part.highlight ? 'react-autosuggest__suggestion-match' : null;

	  return (
	    <span className={className} key={index}>
	      {part.text}
	    </span>
	  );
	})}
      </span>
    );
  }

  onChange = (event, { newValue, method }) => {
    this.setState({
      value: newValue
    });
  }

  onSuggestionSelected = (event, { suggestion }) => {
    const cik = suggestion.cik_str;
    this.props.onSubmit(cik);
  }

  getSuggestionValue = (suggestion) => suggestion.title;

  getSuggestions = (value) => {
    const inputValue = value.trim().toLowerCase();
    const inputLength = inputValue.length;
    const companies = this.state.companies;

    return inputLength === 0 ? [] : companies.filter((comp) => {
      if (comp.title === null || comp.ticker === null) {
	return false;
      }
      const matchString = comp.title.toLowerCase().concat(" ", comp.ticker.toLowerCase());
      let searchValue = inputValue
      if (searchValue !== matchString.substring(0, searchValue.length)) {
	searchValue = " ".concat(searchValue)
      }
      const match = matchString.includes(searchValue);

      return match;
    })
  }

  onSuggestionsFetchRequested = ({ value }) => {
    const allSuggestions = this.getSuggestions(value);
    let suggestions = []
      , titles = []
      , i = 0;
    while (suggestions.length <= 6 && allSuggestions.length > i) {
      let comp = allSuggestions[i]
      const title = comp.title;
      if (!titles.includes(title)) {
	suggestions.push(comp);
	titles.push(title);
      }
      i += 1;
    }
    this.setState({
      suggestions: suggestions
    });
  }

  onSuggestionsClearRequested = () => {
    this.setState({
      suggestions: []
    });
  }

  render() {
    const { value, suggestions } = this.state;

    const inputProps = {
      placeholder: 'type a company name or ticker',
      value,
      onChange: this.onChange,
      type: "text",
    };

    return (
      <Autosuggest
          suggestions={suggestions}
          onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
          onSuggestionsClearRequested={this.onSuggestionsClearRequested}
          onSuggestionSelected={this.onSuggestionSelected}
          getSuggestionValue={this.getSuggestionValue}
          renderSuggestion={this.renderSuggestion}
          highlightFirstSuggestion={true}
          inputProps={inputProps}
          onSubmit={this.props.onSubmit}
      />
    );
  }
}
