// import logo from './logo.svg';
//import './App.css';
import React, { useState, useEffect } from 'react';


import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Alert from 'react-bootstrap/Alert'

import SearchResults from './SearchResults';
import SearchForm from './SearchForm';

import { useTranslation } from 'react-i18next';


function App() {
  const [results, setResults] = useState([]);
  const [resultsEmpty, setResultsEmpty] = useState(false)
  const [isTitleInternal, setIsTitleInternal] = useState("__init")

  const { t, i18n } = useTranslation();

  if (isTitleInternal === "__init") {
    setIsTitleInternal(document.title === "_");
  }


  // note/todo: after integration with webpage a watchdog may be needed, depending on
  //            how the webpage language switch is implemented.
  //               - via query string param - probably will be OK, as reload is expected
  //               - via cookie - watchdog likely to be needed 
  const [language] = useState(i18n.resolvedLanguage);

  useEffect(() => {
    if (isTitleInternal) {
      document.title = t('title')
    }
  }, [language, isTitleInternal]); // eslint-disable-line react-hooks/exhaustive-deps




  // note: Container/Row/Col around SearchForm is added intentionally as a quick way
  //       to ensure consistent alignment between search form and search results
  return (
    <div className="App">
      <div>
        <Container fluid className='px-5'>
          <Row className='w-100'>
            <Col lg={2} className='p-0'>
              <Container fluid className='mt-2 p-0'>
                <Row className='w-100'>
                  <Col className='p-0'>
                    <SearchForm language={language} setResults={setResults} setResultsEmpty={setResultsEmpty}>
                    </SearchForm>
                  </Col>
                </Row>
              </Container>
            </Col>
            <Col lg={10} className='p-0'>
              {resultsEmpty ?
                <Alert variant='light' className='mt-2 text-center'>{t("emptyResults")}</Alert> :
                <SearchResults results={results} ></SearchResults>
              }
            </Col>
          </Row>
        </Container>
      </div>
    </div>

  );
}

export default App;
