import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import { useTranslation } from 'react-i18next';


function SearchResults(props) {

    const { t } = useTranslation();

    const results = props.results;
    let rowSplit = []
    if (results.length > 0) {
        rowSplit.push([])
    }

    for (const res of results) {
        let last = rowSplit.length - 1
        if (rowSplit[last].length === 3) {
            rowSplit.push([])
            last += 1;
        }
        rowSplit[last].push(res)
    }

    return (
        <Container fluid className='mt-2 p-0'>
            {rowSplit.map((newRow, indexRow) =>
                <Row className='w-100 h-25 mb-2 mt-2' key={indexRow}>
                    {newRow.map((res, index) =>
                        <Col key={index} className='equal-height-col w-25'>
                            <Card className="h-100">
                                <Card.Body>
                                    <Card.Title>{res.title}</Card.Title>
                                    <Card.Subtitle className="mb-2 text-muted">{res.institution}</Card.Subtitle>
                                    <Card.Subtitle className="mb-2 text-muted">{t("consumer") + " - " + res.client_type}</Card.Subtitle>
                                    <Card.Text>{res.desc}</Card.Text>
                                </Card.Body>

                                <Card.Footer className="text-muted">

                                    {res.url &&
                                        <Card.Link href={res.url}>{t("webpage")}</Card.Link>
                                    }
                                    {res.email &&
                                        <Card.Link href={"mailto:" + res.email}>{t("contact")}</Card.Link>
                                    }
                                </Card.Footer>
                            </Card>
                        </Col>
                    )}
                </Row>
            )
            }
        </Container>
    )
}


export default SearchResults;