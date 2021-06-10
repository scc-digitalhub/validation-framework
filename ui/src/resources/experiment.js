import * as React from 'react';

import { List, Datagrid, TextField, FunctionField } from 'react-admin';
import { useRedirect, useQuery, Loading, Error } from 'react-admin';
import { Title, Toolbar, TopToolbar, ExportButton, MenuItemLink, SimpleShowLayout } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import ListIcon from '@material-ui/icons/List';

import { SelectButton } from '../fields/select-button';
import { BackButton } from '../fields/back-button';

import { AppContext } from '../contexts/app-context';

import { CheckProjectAndExperiment } from '../utils/common-functions';

const ListActions = (props) => {
    return (
        <TopToolbar>
            <ExportButton key='export-button' />
            <BackButton key='back-button' resource='experiment'/>
        </TopToolbar>
    );
}

export const ExperimentList = (props) => {
    const redirect = useRedirect();
    const currentProject = React.useContext(AppContext).getProject();
    if (!currentProject) {
        redirect('/project');
        return null;
    }
    
    return (
        <List {...props} perPage={50} pagination={false} actions={<ListActions />}>
            <Datagrid rowClick="">
                <TextField source="experiment_id" label="Experiment ID" />
                <TextField source="experiment_name" label="Name" />
                <SelectButton />
            </Datagrid>
        </List>
    );
}

export const ExperimentOverview = props => {
    CheckProjectAndExperiment();
    
    const resource = 'experiment';
    const currentExperiment = React.useContext(AppContext).getExperiment();

    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: resource,
        payload: {
            id: currentExperiment
        }
    });

    if (loading) return <Loading />;
    if (error) return <Error />;
    if (!data) return null;
    
    return (
        <div>
            <Title title={data.experiment_name} />
            <TopToolbar>
                <BackButton resource='experiment' clear={true} />
            </TopToolbar>
            <Card>
                <CardContent>
                    <React.Fragment>
                        <SimpleShowLayout record={data} resource={resource}>
                            <FunctionField label="Name" render={data => <h1> {data.experiment_name} </h1>} />
                            <TextField source="experiment_id" label="Experiment ID" />
                            <TextField source="id" label="ID" />
                        </SimpleShowLayout>
                    </React.Fragment>
                </CardContent>
                
                <Toolbar>
                    <MenuItemLink
                        key='run'
                        to='/run'
                        primaryText='Runs'
                        leftIcon={<ListIcon />}
                        //onClick={onMenuClick}
                        sidebarIsOpen={true}
                    />
                </Toolbar>
            </Card>
        </div>
    );
}