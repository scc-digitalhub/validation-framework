import * as React from 'react';

import { List, Datagrid, TextField, FunctionField } from 'react-admin';
import { TextInput } from 'react-admin';
import { Create, Edit, SimpleForm } from 'react-admin';
import { useRedirect, useQuery, Loading } from 'react-admin';
import { Title, Toolbar, TopToolbar, MenuItemLink, SimpleShowLayout } from 'react-admin';
import { required, regex } from 'react-admin';
import { CreateButton } from 'react-admin';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import ListIcon from '@material-ui/icons/List';
import ClearIcon from '@material-ui/icons/Clear';

import { SelectButton } from '../fields/select-button';
import { EditButton } from 'react-admin';
import { BackButton } from '../fields/back-button';

import { AppContext } from '../contexts/app-context';

import { missingDocumentError } from '../utils/common-functions';

const validateId = [required(), regex(/^[a-zA-Z0-9_-]+$/, 'Allowed characters are lowercase letters, numbers, underscore (_) and hyphen (-).')];
const validateName = regex(/^[a-zA-Z0-9 _-]+$/, 'Allowed characters are lowercase letters, numbers, underscore (_), hyphen (-) and space ( ).');

const clearIcon = <ClearIcon />

const ListActions = (props) => {
    return (
        <TopToolbar>
            <CreateButton key='create-button' />
        </TopToolbar>
    );
}

export const ProjectList = (props) => (
    <List {...props} perPage={50} pagination={false} actions={<ListActions />} >
        <Datagrid rowClick="">
            <TextField source="id" label="ID" />
            <TextField source="name" />
            <EditButton />
            <SelectButton />
        </Datagrid>
    </List>
);

const CreateActions = (props) => {
    return (
        <TopToolbar>
            <BackButton key='back-button' resource='project' label='Cancel' icon={clearIcon} />
        </TopToolbar>
    );
}

export const ProjectCreate = ({ ...props }) => (
    <Create {...props} actions={<CreateActions />}>
        <SimpleForm redirect="list">
            <TextInput source="id" label="ID" validate={validateId} />
            <TextInput source="name" validate={validateName} />
        </SimpleForm>
    </Create>
);

export const ProjectEdit = ({ ...props }) => (
    <Edit undoable={false} {...props} actions={<ListActions />}>
        <SimpleForm >
            <TextField source="id" label="ID" />
            <TextInput source="name" />
        </SimpleForm>
    </Edit>
);

export const ProjectOverview = props => {
    const resource = 'project';
    const currentProject = React.useContext(AppContext).getProject();
    
    const redirect = useRedirect();
    if (!currentProject)
        redirect('/project');
    
    const { data, loading, error } = useQuery({
        type: 'getOne',
        resource: resource,
        payload: {
            id: currentProject
        }
    });

    if (loading)
        return <Loading />;
    if (error || !data)
        return missingDocumentError(resource);
    
    return (
        <React.Fragment>
            <Title title={data.name} />
            <TopToolbar>
                <BackButton resource='project'/>
            </TopToolbar>
            <Card>
                <CardContent>
                    <React.Fragment>
                        <SimpleShowLayout record={data} resource={resource}>
                            <FunctionField label="Name" render={data => <h1> {data.name} </h1>} />
                            <TextField source="id" label="ID" />
                        </SimpleShowLayout>
                    </React.Fragment>
                </CardContent>
                
                <Toolbar>
                    <MenuItemLink
                        key='experiment'
                        to='/experiment'
                        primaryText='Experiments'
                        leftIcon={<ListIcon />}
                    />
                </Toolbar>
            </Card>
        </React.Fragment>
    );
}