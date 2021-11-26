import * as React from 'react';

import { List, Datagrid, TextField, FunctionField, SingleFieldList, ChipField } from 'react-admin';
import { Filter, TextInput } from 'react-admin';
import { useRedirect, useQuery, Loading } from 'react-admin';
import { Title, Toolbar, TopToolbar, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import ListIcon from '@material-ui/icons/List';
import CompareArrowsIcon from '@material-ui/icons/CompareArrows';

import { SelectButton } from '../fields/select-button';
import { BackButton } from '../fields/back-button';
import { TextArrayField } from '../fields/text-array-field';
import { CompareRecentButton } from '../fields/compare-recent-button';

import { AppContext } from '../contexts/app-context';

import { PATH_PROJECT, PATH_RUN, PATH_RUN_COMPARISON_RECENT, RESOURCE_EXPERIMENT } from '../utils/common-constants';
import { CheckProjectAndExperiment, missingDocumentError, makeMenuItemLink } from '../utils/common-functions';

const ListActions = (props) => {
    return (
        <TopToolbar>
            <BackButton key='back-button' resource={RESOURCE_EXPERIMENT} />
        </TopToolbar>
    );
}

const ExperimentFilters = (props) => (
    <Filter {...props}>
        <TextInput label="Search by tags" source="tags" alwaysOn/>
    </Filter>
);

export const ExperimentList = (props) => {
    const redirect = useRedirect();
    const currentProject = React.useContext(AppContext).getProject();
    if (!currentProject) {
        redirect(PATH_PROJECT);
        return null;
    }
    
    return (
        <List {...props}
                perPage={50}
                pagination={false}
                sort={{ field: 'experimentId', order: 'ASC' }}
                actions={<ListActions />}
                filters={<ExperimentFilters/>}
                >
            <Datagrid rowClick="">
                <TextField source="experimentId" label="Experiment ID" />
                <TextField source="experimentName" label="Name" />
                <TextArrayField source="tags">
                    <SingleFieldList>
                        <ChipField />
                    </SingleFieldList>
                </TextArrayField>
                <SelectButton />
            </Datagrid>
        </List>
    );
}

export const ExperimentOverview = props => {
    CheckProjectAndExperiment();
    
    const currentExperiment = React.useContext(AppContext).getExperiment();

    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: RESOURCE_EXPERIMENT,
        payload: {
            id: currentExperiment
        }
    });

    if (loading)
        return <Loading />;
    if (error || !data)
        return missingDocumentError(RESOURCE_EXPERIMENT);
    
    return (
        <React.Fragment>
            <Title title={data.experimentName} />
            <TopToolbar>
                <CompareRecentButton key='compare-recent-button' />
                <BackButton key='back-button' resource={RESOURCE_EXPERIMENT} clear={true} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <React.Fragment>
                        <SimpleShowLayout record={data} resource={RESOURCE_EXPERIMENT}>
                            <FunctionField label="Name" render={data => <h1> {data.experimentName} </h1>} />
                            <TextField source="experimentId" label="Experiment ID" />
                            <TextArrayField source="tags">
                                <SingleFieldList>
                                    <ChipField />
                                </SingleFieldList>
                            </TextArrayField>
                            <TextField source="id" label="ID" />
                        </SimpleShowLayout>
                    </React.Fragment>
                </CardContent>
                
                <Toolbar>
                    {makeMenuItemLink('run', PATH_RUN, 'Runs', <ListIcon />)}
                    {makeMenuItemLink('run-comparison-recent', PATH_RUN_COMPARISON_RECENT, 'Compare recent runs', <CompareArrowsIcon />)}
                </Toolbar>
            </Card>
        </React.Fragment>
    );
}