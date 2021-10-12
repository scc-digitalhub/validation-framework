import * as React from 'react';

import { useQuery, Loading, FunctionField } from 'react-admin';
import { Title, TopToolbar, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import validationComparison from './validation';
import executionComparison from './execution';
import profileComparison from './profile';

import { BackButton } from '../../fields/back-button';
import { genericError } from '../../utils/common-functions';

export const RunComparisonDetail = props => {
    const resource = 'run-comparison';
    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: resource,
        payload: {
            ids: props.match.params.selectedIds
        }
    });
    
    if (loading)
        return <Loading />;
    if (error || !data || !data.runs)
        return genericError(resource, "Error while retrieving comparison.");
    
    return (
        <React.Fragment>
            <Title title="Run comparison" />
            <TopToolbar>
                <BackButton resource={resource} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <SimpleShowLayout record={data} resource={resource}>
                        <FunctionField label="Results of validation" render={validationComparison} />
                        <FunctionField label="Execution information" render={executionComparison} />
                        <FunctionField label="Data profile" render={profileComparison} />
                    </SimpleShowLayout>
                </CardContent>
            </Card>
        </React.Fragment>
    );
}