package it.smartcommunitylab.validationstorage.common;

public class ValidationStorageConstants {

    // Constants used to determine the path of certain end-points
    public static final String EXPERIMENT = "experiment";
    public static final String RUN = "run";
    public static final String PACKAGE = "package";
    public static final String STORE = "store";
    public static final String RESOURCE = "resource";
    public static final String SCHEMA = "schema";
    public static final String CONSTRAINT = "constraint";
    public static final String RUN_CONFIG = "run-config";
    
    public static final String ARTIFACT_METADATA = "artifact-metadata";
    public static final String DATA_RESOURCE = "data-resource";
    public static final String DATA_PROFILE = "data-profile";
    public static final String RUN_ENVIRONMENT = "run-environment";
    public static final String RUN_METADATA = "run-metadata";
    public static final String SHORT_REPORT = "short-report";
    public static final String SHORT_SCHEMA = "short-schema";
    
    // RunMetadata documents act as representatives for the run they refer to, and are used as base to build
    // run summaries. This is especially important for the UI, which bases its list of runs on run summaries.
    // These constants are for run summary end-points.
    public static final String RUN_RICH = "run-rich";
    public static final String RUN_RICH_RECENT = "run-rich-recent";
    public static final int RECENT_RUNS_NUMBER = 5;
    
    // Date format and contents field for dates in RunMetadata documents
    public static final String DATE_FORMAT = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX";
    public static final String FIELD_RUN_METADATA_TS = "created";
    
    // Conditions for PreAuthorize and similar annotations
    public static final String PREAUTH_PROJECTID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + #projectId)";
    public static final String PREAUTH_ID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + #id)";
    public static final String PREAUTH_REQUEST_ID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + #request.getId())";
    public static final String POSTFILTER_ID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + filterObject.getId())";
    
    // Patterns to check validity of certain fields
    public static final String NAME_PATTERN = "^[a-zA-Z0-9_-]+$";
    public static final String TITLE_PATTERN = "^[a-zA-Z0-9 _-]+$";
    
}
