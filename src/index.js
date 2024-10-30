import React from 'react';
import ReactDOM from 'react-dom';
import SearchBar from './searchbar.js';
import ExcelSheet from './excel_sheet.js';
import Button from 'react-bootstrap/Button';
import ListGroup from 'react-bootstrap/ListGroup';
import Spinner from 'react-bootstrap/Spinner';
import logo from './logo.png';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const base_url = "https://data.sec.gov/submissions/CIK{cik}.json";

class PopUp extends React.Component {
  handleClick = () => {
    this.props.toggle();
  }

  render () {
    return (
      <div className="excelModal">
	<div className="modal_content">
	  <button className="close btn btn-secondary" onClick={this.handleClick}>
	    &times;
	  </button>
	  <ExcelSheet/>
	</div>
      </div>
    );
  }
}

class FilingButton extends React.Component {
  handleClick = () => {
    this.props.onClick(this.href());
  }

  href() {
    const baseURL = "https://www.sec.gov/Archives/edgar/data/{cik}/{num}";
    const cik = this.props.cik;
    var num = this.props.filing.accessionNumber;
    const doc = this.props.filing.primaryDocument;
    if (doc) {
      return baseURL.replace("{cik}", cik).replace("{num}", num.replaceAll("-","")) + `/${doc}`;
    } else {
      return baseURL.replace("{cik}", cik).replace("{num}", num) + ".txt";
    }
  }

  render() {
    const dateString = `${this.props.filing.form} ${this.props.filing.reportDate}`;
    return (
      <Button onClick={this.handleClick}>
	{dateString}
      </Button>
    );
  }
}

function FilingLink(props) {
  const link = props.link;

  if (link) {
    return (
      <div className="docLink">
	Direct link:&nbsp;&nbsp;
	<a href={link} target="_blank" rel="noreferrer">{link}</a>
      </div>
    );
  }
  return null
}

function Filing(props) {
  const loading = props.loading;
  const html = props.html;

  if (loading) {
    return (
      <div className="loading">
	<div className="loadingText">
	  <span>Loading document...</span>
	</div>
	<div></div>
	<div>
	  <Spinner animation="border" role="status">
	    <span className="visually-hidden">Loading...</span>
	  </Spinner>
	</div>
      </div>
    );
  }
  return <div dangerouslySetInnerHTML={{__html: html}}></div>
}

function InFilingLinks(props) {
  const html = props.html;
  const scanning = props.scanning;

  if (scanning) {
    return (
      <div className="loading">
	<div className="loadingText">
	  <span>Scanning document...</span>
	</div>
	<div></div>
	<div>
	  <Spinner animation="border" role="status">
	    <span className="visually-hidden">Loading...</span>
	  </Spinner>
	</div>
      </div>
    );
  } else if (html) {
    return (
      <div>
	<span className="sidebarTitle">&nbsp;Go To:</span>
	<ListGroup>
	  <ListGroup.Item>
	    <a href="#IncomeStatement">Income Statement</a>
	    {/*<a href="#IncomeStatementButton">Income Statement</a>*/}
	  </ListGroup.Item>
	  <ListGroup.Item>
	    <a href="#BalanceSheet">Balance Sheet</a>
	    {/*<a href="#BalanceSheetButton">Balance Sheet</a>*/}
	  </ListGroup.Item>
	  <ListGroup.Item>
	    {/*<a href="#CashFlowsButton">Cash Flows</a>*/}
	    <a href="#CashFlows">Cash Flows</a>
	  </ListGroup.Item>
	</ListGroup>
      </div>
    );
  }
  return null
}

function FilingDateButtons(props) {
  const noFilings = props.noFilings;
  const filings = props.filings;
  const onButtonClick = props.onButtonClick;
  const cik = props.cik;

  if (noFilings) {
    return (
      <div className="noFilingsMessage">
	<span>Couldn't find any 10-Q or 10-K filings for this ticker</span>
      </div>
    );
  } else if (filings.length) {
    const filingButtons = filings.map((filing, index) => {
      return (
	<li key={index}>
	  <FilingButton
	    onClick={onButtonClick}
	    filing={filing}
	    cik={cik}
	  />
	</li>
      );
    });
    return (
      <div className="dates">
	<span className="sidebarTitle">&nbsp;Filings:</span>
	<div className="dateButtons">
	  <ul className="dateList">
	    {filingButtons}
	  </ul>
	</div>
      </div>
    );
  }
  return null;
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filings: [],
      filingHtml: '',
      filingLink: '',
      popped: false,
      loading: false,
      scanning: false,
      noFilings: false,
    }
  
    this.handleSearchBarSubmit = this.handleSearchBarSubmit.bind(this);
    this.handleDateClick = this.handleDateClick.bind(this);
    this.togglePop = this.togglePop.bind(this);
  }

  handleSearchBarSubmit(cik) {
    this.setState({
      filingHtml: '',
      filingLink: '',
      filings: [],
    });
    var long_cik = "0000000000" + cik;
    long_cik = long_cik.substr(long_cik.length-10, 10);
    const url = base_url.replace("{cik}", long_cik);
    let headers = new Headers({
      "Content-Type": "application/json",
    });
    fetch(/*http://localhost:5000*/"/api/filings-data", {
      method: "POST",
      headers: headers,
      body: JSON.stringify(url),
    }).then(res => {
      return res.json()
    }).then(res => {
      const recent = res["recent"];
      //const moreFiles = res["files"];
      const annualOrQuarterly = this.filterAnnualOrQuarterly(recent);
      this.setState({
	filings: annualOrQuarterly,
	cik: cik,
	noFilings: (!annualOrQuarterly.length),
      });
    }).catch(error => {
      console.error('Error:', error);
    });
  }

  filterAnnualOrQuarterly(data) {
    const types = ["10-K", "10-Q", "S-1"];
    var keys = Object.keys(data);
    const forms = data.form;
    var annualOrQuarterly = []; 
    for (let i = 0; i < forms.length; i++) {
      if (types.includes(forms[i])) {
	annualOrQuarterly.push(keys.reduce((dic, key) => ((dic[key] = data[key][i], dic)), {}));
      }
    }
    return annualOrQuarterly
  }

  handleDateClick(url) {
    //fetch("http://localhost:5000/api/filing-html", {
    this.setState({
      loading: true,
      filingLink: '',
    });
    this.getUnmodifiedHtml(url);
    this.getModifiedHtml(url);
  }

  getUnmodifiedHtml(url) {
    fetch(/*http://localhost:5000*/"/api/filing-html", {
      method: "POST",
      headers: {"content-type": "application/json",},
      body: JSON.stringify(url)
    })
      .then(res => res.json())
      .then(
	res => {
	  this.setState({
	    loading: false,
	    filingHtml: res["html"],
	    filingLink: url,
	  });
	})
  }

  getModifiedHtml(url) {
    this.setState({
      scanning: true,
    });
    fetch(/*http://localhost:5000*/"/api/filing-html-modified", {
      method: "POST",
      headers: {"content-type": "application/json",},
      body: JSON.stringify(url)
    })
      .then(res => res.json())
      .then(
	res => {
	  this.setState({
	    scanning: false,
	    filingHtml: res["html"],
	    filingLink: url,
	  });
	  this.configureButtons();
	})
  }

  configureButtons() {
    const buttons = document.getElementsByClassName('tableButton');
    for (let i = 0; i < buttons.length; i++) {
      const id = buttons.item(i).id;
      buttons.item(i).onclick = () => {this.tableButtonClick(id);}
    }
  }

  togglePop() {
    const currState = this.state.popped;
    this.setState({
      popped: !currState,
    });
  }

  tableButtonClick(id) {
    const tableClass = id.replace("Button","");
    const tableHtml = document.getElementsByClassName(tableClass).item(0).outerHTML;
    let headers = new Headers({
      "Content-Type": "application/json",
    });
    fetch(/*http://localhost:5000*/"/api/convert-excel", {
      method: "POST",
      headers: headers,
      body: JSON.stringify(tableHtml),
    }).then(this.togglePop())
  }

  render() {
    return (
      <div>
	<div className="searchBar_Main">
	  <img className='logo' src={logo} alt="Logo" />
	  <div className="searchBar_Container">
	    <SearchBar
	      onSubmit={this.handleSearchBarSubmit}
	    />
	  </div>
	</div>
	<FilingLink
	  link={this.state.filingLink}
	/>
	<div className="mainContainer">
	  <div className="sidebar">
	    <FilingDateButtons
	      noFilings = {this.state.noFilings}
	      filings = {this.state.filings}
	      onButtonClick = {this.handleDateClick}
	      cik = {this.state.cik}
	    />
	    <div className="tableLinks">
	      <InFilingLinks
		html={this.state.filingHtml}
		scanning={this.state.scanning}
	      />
	    </div>
	  </div>
	  <div className="filing">
	    <Filing
	      loading={this.state.loading}
	      html={this.state.filingHtml}
	    />
	  </div>
	  {this.state.popped ? <PopUp toggle={this.togglePop} /> : null}
	</div>
      </div>
    );
  }
}

ReactDOM.render(
  <App />,
  document.getElementById("root")
);
