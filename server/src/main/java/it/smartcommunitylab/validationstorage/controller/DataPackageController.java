package it.smartcommunitylab.validationstorage.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylab.validationstorage.common.ValidationStorageConstants;
import it.smartcommunitylab.validationstorage.service.DataPackageService;

@RestController
@RequestMapping(value = "/api/project")
@PreAuthorize(ValidationStorageConstants.PREAUTH_PROJECTID)
public class DataPackageController {
    @Autowired
    private DataPackageService service;
}
