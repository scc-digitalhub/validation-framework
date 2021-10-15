import * as React from 'react';

import { fetchUtils } from 'react-admin';

import { ENDPOINT_PROJECT, ENDPOINT_EXPERIMENT, ENDPOINT_RUN, ENDPOINT_RUN_RICH, ENDPOINT_RUN_RICH_RECENT,
 ENDPOINT_ARTIFACT_METADATA, RESOURCE_PROJECT, RESOURCE_EXPERIMENT, RESOURCE_RUN, RESOURCE_RUN_COMPARISON,
 RESOURCE_RUN_COMPARISON_RECENT, RESOURCE_ARTIFACT_METADATA } from './utils/common-constants';

const backendUrl = process.env.REACT_APP_BACKEND_ADDRESS;

const httpClient = (url, options = {}) => {
    return fetchUtils.fetchJson(url, options);
};

export class DataProvider extends React.Component {
    constructor(props) {
        super(props);
        this.getProject = props.getProject;
        this.getExperiment = props.getExperiment;
    }
    
    getList(resource, params) {
        const page = params.pagination.page;
        const size = params.pagination.perPage;
        const sort = params.sort.field + ',' + params.sort.order;
        const query = 'page=' + (page-1) + '&size=' + size + '&sort=' + sort;
        
        let url = `${backendUrl}`+ENDPOINT_PROJECT;
        
        switch(resource) {
            case RESOURCE_PROJECT:
                url += `?${query}`;
                break;
            case RESOURCE_EXPERIMENT:
                if (!this.getProject())
                    return Promise.reject(new Error('Project not set.'));
                url += `/${this.getProject()}`+ENDPOINT_EXPERIMENT+`?${query}`;
                break;
            case RESOURCE_RUN:
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                url += `/${this.getProject()}`+ENDPOINT_EXPERIMENT+`/${this.getExperiment()}`+ENDPOINT_RUN+`?${query}`;
                break;
            case RESOURCE_RUN_COMPARISON:
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                if (!params.ids)
                    return Promise.reject(new Error('IDs are missing.'));
                url += `/${this.getProject()}`+ENDPOINT_EXPERIMENT+`/${this.getExperiment()}`+ENDPOINT_RUN_RICH+`/${params.ids}`;
                break;
            case RESOURCE_RUN_COMPARISON_RECENT:
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                url += `/${this.getProject()}`+ENDPOINT_EXPERIMENT+`/${this.getExperiment()}`+ENDPOINT_RUN_RICH_RECENT;
                break;
            case RESOURCE_ARTIFACT_METADATA:
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                if (!params.id)
                    return Promise.reject(new Error('Run ID is null.'));
                url += `/${this.getProject()}`+ENDPOINT_EXPERIMENT+`/${this.getExperiment()}`+ENDPOINT_RUN+`/${params.id}`+ENDPOINT_ARTIFACT_METADATA+`?${query}`;
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
        let url = `${backendUrl}` + ENDPOINT_PROJECT;
        switch (resource) {
            case RESOURCE_PROJECT:
                url += `/${params.id}`;
                break;
            case RESOURCE_EXPERIMENT:
                if (!this.getProject())
                    return Promise.reject(new Error('Project not set.'));
                url += `/${this.getProject()}`+ENDPOINT_EXPERIMENT+`/${params.id}`;
                break;
            case RESOURCE_RUN:
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                if (!params.id)
                    return Promise.reject(new Error('Run ID is null.'));
                url += `/${this.getProject()}`+ENDPOINT_EXPERIMENT+`/${this.getExperiment()}`+ENDPOINT_RUN+`/${params.id}`;
                break;
            default:
                if (!this.getProject() || !this.getExperiment())
                    return Promise.reject(new Error('Project or experiment not set.'));
                if (!params.id)
                    return Promise.reject(new Error('Run ID is null.'));
                url += `/${this.getProject()}`+ENDPOINT_EXPERIMENT+`/${this.getExperiment()}`+ENDPOINT_RUN+`/${params.id}/${resource}`;
        }
        
        return httpClient(url).then( ({ json }) => ({
            data: json,
        }));
    }
    
    create(resource, params) {
        if (resource === RESOURCE_PROJECT) {
            return httpClient(`${backendUrl}/${resource}`, {
                method: 'POST',
                body: JSON.stringify(params.data),
            }).then(({ json }) => ({ data: { ...params.data, id: json.id } }));
        } else {
            return Promise.reject(new Error('Only project documents may be created.'));
        }
    }
    
    update(resource, params) {
        if (resource === RESOURCE_PROJECT) {
            if (!params.id)
                return Promise.reject(new Error('Project ID is null.'));
            return httpClient(`${backendUrl}`+ENDPOINT_PROJECT+`/${params.id}`, {
                method: 'PUT',
                body: JSON.stringify(params.data),
            }).then(({ json }) => ({ data: json }));
        } else {
            return Promise.reject(new Error('Only project documents may be updated.'));
        }
    }
    
    delete(resource, params) {
        let url = `${backendUrl}`+ENDPOINT_PROJECT;
        if (resource !== RESOURCE_PROJECT)
            url += `/${this.getProject()}/${resource}`;
        
        if (!params.id)
            return Promise.reject(new Error('Resource ID is null.'));
        return httpClient(`${url}/${params.id}`, {
            method: 'DELETE',
        }).then(response => ({ data: '' }));
    }
    
    deleteMany(resource, params) {
        let url = `${backendUrl}`+ENDPOINT_PROJECT;
        if (resource !== RESOURCE_PROJECT)
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