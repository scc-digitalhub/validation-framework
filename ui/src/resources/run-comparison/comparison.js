import * as React from 'react';

import { useQuery, Loading, FunctionField } from 'react-admin';
import { Title, TopToolbar, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import validationComparison from './validation';
import executionComparison from './execution';
import profileComparison from './profile';

import { BackButton } from '../../fields/back-button';
import { RESOURCE_RUN_COMPARISON, RESOURCE_RUN_COMPARISON_RECENT } from '../../utils/common-constants';
import { genericError } from '../../utils/common-functions';

export const RunComparisonRecentDetail = props => {
    return RunComparison(props, RESOURCE_RUN_COMPARISON_RECENT);
}

export const RunComparisonDetail  = props => {
    return RunComparison(props, RESOURCE_RUN_COMPARISON);
}

export const RunComparison = (props, resource) => {
    let { data, loading, error } = useQuery({
        type: 'getList',
        resource: resource,
        payload: {
            ids: props.match.params.requested,
            pagination: {
                page: 1,
                perPage: 50
            },
            sort: {
                field: "created",
                order: "DESC"
            }
        }
    });
    
    if (loading)
        return <Loading />;
    if (error || !data)
        return genericError(resource, "Error while retrieving comparison.");
    
    data = {
        runs: data,
        requested: props.match.params.requested
    }
    
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