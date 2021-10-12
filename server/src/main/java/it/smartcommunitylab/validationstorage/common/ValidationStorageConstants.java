package it.smartcommunitylab.validationstorage.common;

public class ValidationStorageConstants {

    // Constants used to determine the path of certain end-points
    public static final String ARTIFACT_METADATA = "artifact-metadata";
    public static final String DATA_RESOURCE = "data-resource";
    public static final String DATA_PROFILE = "data-profile";
    public static final String EXPERIMENT = "experiment";
    public static final String RUN_ENVIRONMENT = "run-environment";
    public static final String RUN_METADATA = "run-metadata";
    public static final String SHORT_REPORT = "short-report";
    public static final String SHORT_SCHEMA = "short-schema";
    public static final String RUN_COMPARISON = "run-comparison";
    public static final String RUN_COMPARISON_RECENT = "recent";
    
    // RunMetadata documents act as representatives for the run they refer to. This is especially true for the UI,
    // where all data related to a run is nested within the RunMetadata document. To make this nesting more explicit,
    // UI end-points will use this constant for the portion of the path that identifies a run.
    public static final String RUN = "run";
    
    // Date format and contents field for dates in RunMetadata documents
    public static final String DATE_FORMAT = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX";
    public static final String FIELD_RUN_METADATA_TS = "created";
    
    // Conditions for PreAuthorize and similar annotations
    public static final String PREAUTH_PROJECTID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + #projectId)";
    public static final String PREAUTH_ID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + #id)";
    public static final String PREAUTH_REQUEST_ID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + #request.getId())";
    public static final String POSTFILTER_ID = "hasAuthority(@authenticationProperties.getProjectAuthorityPrefix() + filterObject.getId())";
    
    // Patterns to check validity of certain fields
    public static final String ID_PATTERN = "^[a-zA-Z0-9_-]+$";
    public static final String NAME_PATTERN = "^[a-zA-Z0-9 _-]+$";
    
}
