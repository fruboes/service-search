import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import { useTranslation } from 'react-i18next';
import InputGroup from 'react-bootstrap/InputGroup'



function SearchForm(props) {
    const [queryString, setQueryString] = useState("");
    const [clientTypes, setClientTypes] = useState([]);
    const [clientTypesCheckboxStates, setClientTypesCheckboxStates] = useState({})
    const [serviceTypesCheckboxStates, setServiceTypesCheckboxStates] = useState({})

    const [serviceTypes, setServiceTypes] = useState([]);


    const { t } = useTranslation();

    useEffect(() => {
        let url = '/getFilterValues?' + new URLSearchParams({
            lng: props.language
        })

        fetch(url)
            .then(res => res.json())
            .then(
                (result) => {
                    setClientTypes(result.client_type);
                    setServiceTypes(result.service_type);
                    setClientTypesCheckboxStates(result.client_type.reduce((a, v) => ({ ...a, [v[0]]: false }), {}))
                    setServiceTypesCheckboxStates(result.service_type.reduce((a, v) => ({ ...a, [v[0]]: false }), {}))

                })
    }, [props.language])



    const handleChange = (e) => {
        setQueryString(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const selectedClientTypes = Object.keys(clientTypesCheckboxStates).filter(x => clientTypesCheckboxStates[x]);
        const selectedServiceTypes = Object.keys(serviceTypesCheckboxStates).filter(x => serviceTypesCheckboxStates[x]);

        if (queryString || selectedClientTypes.length > 0 || selectedServiceTypes.length > 0) {
            let url = '/query?' + new URLSearchParams({
                q: queryString,
                clientTypes: selectedClientTypes,
                serviceTypes: selectedServiceTypes,
                lng: props.language
            })

            fetch(url)
                .then(res => res.json())
                .then(
                    (result) => {
                        props.setResults(result);
                        if (result.length === 0) {
                            props.setResultsEmpty(true)
                        }
                    },
                    // Note: it's important to handle errors here
                    // instead of a catch() block so that we don't swallow
                    // exceptions from actual bugs in components.
                    (error) => {
                        console.log("ERRR", error) // TODO
                        props.setResults([])
                        props.setResultsEmpty(false)
                    }
                )
        } else {
            props.setResults([])
            props.setResultsEmpty(false)
        }
    }


    return (
        <Form onSubmit={handleSubmit} className='w-100'>
            <InputGroup className='w-auto'>
                <Form.Control type="text"
                    placeholder="..."
                    value={queryString}
                    onChange={handleChange}
                    className='mr-2'
                    style={{ boxShadow: 'none' }}
                />
                <Button variant="primary" type="submit" className='ml-2'>
                    {t("search")}
                </Button>
            </InputGroup>
            <Form.Label className='mt-3'>{t("consumer").toUpperCase()}</Form.Label>
            <Form.Group className="mb-3" controlId="formBasicCheckbox">
                {clientTypes.map((val, index) =>
                    <Form.Check
                        type="checkbox"
                        value={clientTypesCheckboxStates[val[0]]}
                        onChange={() => setClientTypesCheckboxStates({ ...clientTypesCheckboxStates, [val[0]]: !clientTypesCheckboxStates[val[0]] })}
                        label={val[0] + " (" + val[1] + ")"}
                        id={"clientType_" + index}
                        key={index} />
                )}
            </Form.Group>

            <Form.Label className='mt-3'>{t("serviceType").toUpperCase()}</Form.Label>
            <Form.Group className="mb-3" controlId="formBasicCheckbox">
                {serviceTypes.map((val, index) =>
                    <Form.Check
                        type="checkbox"
                        value={serviceTypesCheckboxStates[val[0]]}
                        onChange={() => setServiceTypesCheckboxStates({ ...serviceTypesCheckboxStates, [val[0]]: !serviceTypesCheckboxStates[val[0]] })}
                        label={val[0] + " (" + val[1] + ")"}
                        id={"serviceType_" + index}
                        key={index} />
                )}
            </Form.Group>
        </Form>


    )

}

export default SearchForm