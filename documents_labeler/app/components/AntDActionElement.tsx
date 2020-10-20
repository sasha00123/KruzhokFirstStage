import { Button } from 'antd';
import React from 'react';
import { ActionProps } from 'react-querybuilder/types';

const AntDActionElement = ({ className, handleOnClick, label, title }: ActionProps) => (
  <Button type="primary" className={className} title={title} onClick={(e) => handleOnClick(e)}>
    {label}
  </Button>
);

AntDActionElement.displayName = 'AntDActionElement';

export default AntDActionElement;
