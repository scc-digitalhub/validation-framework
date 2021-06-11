import * as React from 'react';

import { fetchUtils } from 'react-admin';

import { authProvider } from './auth/auth-provider';

const apiUrl = process.env.REACT_APP_BACKEND_ADDRESS;

const httpClient = (url, options = {}) => {
    // if (!options.headers) {
        // options.headers = new Headers({ Accept: 'application/json' });
    // }
    
    // return authProvider.getAuth().then((token) => {
        // options.headers.set('Authorization', `Bearer ${token}`);
        // return fetchUtils.fetchJson(url, options);
    // });
    
    return fetchUtils.fetchJson(url, options);
};

export class DataProvider extends React.Component {
    constructor(props) {
        super(props);
        this.getProject = props.getProject;
        this.getExperiment = props.getExperiment;
    }
    
    getList(resource, params) {
        console.log(apiUrl);
        const page = params.pagination.page;
        const size = params.pagination.perPage;
        const sort = params.sort.field + ',' + params.sort.order;
        const query = 'page=' + (page-1) + '&size=' + size + '&sort=' + sort;
        
        let url = `${apiUrl}/project`;
        
        switch(resource) {
            case 'project':
                url += `?${query}`;
                break;
            case 'experiment':
                if (!this.getProject())
                    return Promise.reject(new Error('Project not set.'));
                url += `/${this.getProject()}/experiment?${query}`;
                break;
            case 'run':
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                url += `/${this.getProject()}/experiment/${this.getExperiment()}/run?${query}`;
                break;
            case 'artifact-metadata':
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                if (!params.id)
                    return Promise.reject(new Error('Run ID is null.'));
                url += `/${this.getProject()}/experiment/${this.getExperiment()}/run/${params.id}/artifact-metadata?${query}`;
                break;
            default:
                return Promise.reject(new Error('Invalid getList request.'));
        }
        
		return httpClient(url).then( ({ json }) => ({
            data: json,
            total: json.length,
        }));
    }
    
    getOne(resource, params) {
        let url = `${apiUrl}/project`;
        switch (resource) {
            case 'project':
                url += `/${params.id}`;
                break;
            case 'experiment':
                if (!this.getProject())
                    return Promise.reject(new Error('Project not set.'));
                url += `/${this.getProject()}/experiment/${params.id}`;
                break;
            case 'run':
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                if (!params.id)
                    return Promise.reject(new Error('Run ID is null.'));
                url += `/${this.getProject()}/experiment/${this.getExperiment()}/run/${params.id}`;
                break;
            default:
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                if (!params.id)
                    return Promise.reject(new Error('Run ID is null.'));
                url += `/${this.getProject()}/experiment/${this.getExperiment()}/run/${params.id}/${resource}`;
        }
        
        return httpClient(url).then( ({ json }) => ({
            data: json,
        }));
    }
    
    create(resource, params) {
        if (resource === 'project') {
            return httpClient(`${apiUrl}/${resource}`, {
                method: 'POST',
                body: JSON.stringify(params.data),
            }).then(({ json }) => ({
                data: { ...params.data, id: json.id },
            }));
        } else {
            return Promise.reject(new Error('Only project documents may be created.'));
        }
    }
    
    update(resource, params) {
        if (resource === 'project') {
            if (!params.id)
                return Promise.reject(new Error('Project ID is null.'));
            return httpClient(`${apiUrl}/project/${params.id}`, {
                method: 'PUT',
                body: JSON.stringify(params.data),
            }).then(({ json }) => ({ data: json }));
        } else {
            return Promise.reject(new Error('Only project documents may be updated.'));
        }
    }
    
    delete(resource, params) {
        let url = `${apiUrl}/project`;
        if (resource !== 'project')
            url += `/${this.getProject()}/${resource}`;
        
        if (!params.id)
            return Promise.reject(new Error('Resource ID is null.'));
        return httpClient(`${url}/${params.id}`, {
            method: 'DELETE',
        }).then(response => ({ data: '' }));
    }
    
    deleteMany(resource, params) {
        let url = `${apiUrl}/project`;
        if (resource !== 'project')
            url += `/${this.getProject()}/${resource}`;
        
        return Promise.all(
            params.ids.map(id =>
                httpClient(`${url}/${id}`, {
                    method: 'DELETE',
                })
            )
        ).then(responses => ({ data: [] }));
    }
}