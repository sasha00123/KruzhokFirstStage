import routes from '../../constants/routes.json';
import { Link } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import QueryBuilder, { formatQuery } from 'react-querybuilder';

import styles from './Deps.css';

import 'react-querybuilder/dist/query-builder.scss';


export default function Deps(): JSX.Element {
  const [json, setJson] = useState();
  const [image, setImage] = useState();
  const [fields, setFields] = useState();


  useEffect(() => {
    const imageString = localStorage.getItem('image');
    if (imageString !== null) {
      const parsedImage = JSON.parse(imageString);
      console.log(parsedImage);
      setImage(parsedImage);
      setFields(parsedImage.regions.map(region => {
        return { name: region.cls, label: region.cls };
      }));
    }
  }, []);

  return <>
    <Container>
      <Row>
        <Link to={routes.ANNOTATIONS}>
          Back
        </Link>
      </Row>

      {fields != null &&
      <Row>
        <QueryBuilder
          fields={fields} onQueryChange={setJson}
          operators={[{ name: 'empty', label: 'is empty' }, { name: 'notEmpty', label: 'is not empty' }]}
          showNotToggle={true}
        />
      </Row>
      }

      {image != null &&
      <Row>
        <Col className="d-flex">
          <img src={image.src} alt="image" className={`${styles.img} mx-auto`}/>
        </Col>
      </Row>
      }

      {json != null &&
        <>
          <h1>Copy this code</h1>
          <pre>
          {formatQuery(json, 'json')}
          </pre>
        </>
        }
    </Container>
  </>;
}
