/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
export interface MetricBase {
  /** The result of the operation */
  readonly result?: Result;
  /** The reason for a metric or exception depending on context */
  readonly reason?: string;
  /** The duration of the operation in milliseconds */
  readonly duration?: number;
  /** A flag indicating that the metric was not caused by the user. */
  readonly passive?: boolean;
  /** @deprecated Arbitrary "value" of the metric. */
  readonly value?: number;
}

export interface ApigatewayCopyUrl extends MetricBase {}

export interface ApigatewayInvokeLocal extends MetricBase {
  /** The lambda runtime */
  readonly runtime?: Runtime;
  /** Any valid HTTP method (GET/HEAD/etc) */
  readonly httpMethod?: string;
  /** If the action was run in debug mode or not */
  readonly debug: boolean;
  /** Lambda architecture identifier */
  readonly lambdaArchitecture?: LambdaArchitecture;
}

export interface ApigatewayInvokeRemote extends MetricBase {
  /** Any valid HTTP method (GET/HEAD/etc) */
  readonly httpMethod?: string;
}

export interface ApigatewayStartLocalServer extends MetricBase {}

export interface ApprunnerOpenServiceUrl extends MetricBase {}

export interface ApprunnerCopyServiceUrl extends MetricBase {}

export interface ApprunnerCreateService extends MetricBase {
  /** The source artifact of an App Runner service */
  readonly appRunnerServiceSource: AppRunnerServiceSource;
}

export interface ApprunnerPauseService extends MetricBase {}

export interface ApprunnerResumeService extends MetricBase {}

export interface ApprunnerDeleteService extends MetricBase {
  /** The current state of the App Runner service */
  readonly appRunnerServiceStatus?: AppRunnerServiceStatus;
}

export interface ApprunnerStartDeployment extends MetricBase {}

export interface ApprunnerViewApplicationLogs extends MetricBase {}

export interface ApprunnerViewServiceLogs extends MetricBase {}

export interface AwsCopyArn extends MetricBase {
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType: string;
}

export interface AwsDeleteResource extends MetricBase {
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType: string;
}

export interface AwsSetCredentials extends MetricBase {
  /** The type of credential that was selected */
  readonly credentialType?: CredentialType;
  /** Where credentials are stored or retrieved from */
  readonly credentialSourceId?: CredentialSourceId;
}

export interface AwsSetRegion extends MetricBase {}

export interface AwsSetPartition extends MetricBase {
  /** The ID of the partition that was selected */
  readonly partitionId: string;
}

export interface AwsOpenCredentials extends MetricBase {}

export interface AwsOpenUrl extends MetricBase {
  /** The url associated with a metric */
  readonly url?: string;
}

export interface AwsSaveCredentials extends MetricBase {}

export interface AwsModifyCredentials extends MetricBase {
  /** The type of modification performed on the credentials */
  readonly credentialModification: CredentialModification;
  /** The source of the operation */
  readonly source: string;
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
}

export interface AwsLoadCredentials extends MetricBase {
  /** Where credentials are stored or retrieved from */
  readonly credentialSourceId: CredentialSourceId;
}

export interface AwsCreateCredentials extends MetricBase {}

export interface AwsInjectCredentials extends MetricBase {
  /** A free-text field to record runtimes that may be separate from Lambda runtimes */
  readonly runtimeString?: string;
}

export interface AwsValidateCredentials extends MetricBase {
  /** The type of credential that was selected */
  readonly credentialType?: CredentialType;
  /** Where credentials are stored or retrieved from */
  readonly credentialSourceId?: CredentialSourceId;
}

export interface AwsRefreshCredentials extends MetricBase {
  /** The type of credential that was selected */
  readonly credentialType?: CredentialType;
  /** Where credentials are stored or retrieved from */
  readonly credentialSourceId?: CredentialSourceId;
  /** Length of time, in milliseconds, that an authentication session has lived for. Useful for determining how frequently a user has to reauthenticate. */
  readonly sessionDuration?: number;
}

export interface AwsLoginWithBrowser extends MetricBase {
  /** The type of credential that was selected */
  readonly credentialType?: CredentialType;
  /** Where credentials are stored or retrieved from */
  readonly credentialSourceId?: CredentialSourceId;
}

export interface AwsHelp extends MetricBase {
  /** A generic name metadata */
  readonly name?: string;
}

export interface AwsHelpQuickstart extends MetricBase {}

export interface AwsShowExtensionSource extends MetricBase {}

export interface AwsRefreshExplorer extends MetricBase {}

export interface AwsExpandExplorerNode extends MetricBase {
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType: string;
}

export interface AwsReportPluginIssue extends MetricBase {}

export interface BeanstalkDeploy extends MetricBase {
  /** Whether or not the deploy targets a new destination (true) or an existing destination (false) */
  readonly initialDeploy: boolean;
  /** A generic name metadata */
  readonly name?: string;
  /** Application framework being used */
  readonly framework?: string;
  /** Whether or not AWS X-Ray is enabled */
  readonly xrayEnabled?: boolean;
  /** Whether or not Elastic Beanstalk enhanced health reporting and monitoring is being used */
  readonly enhancedHealthEnabled?: boolean;
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
  /** The source of the operation */
  readonly source?: string;
}

export interface BeanstalkPublishWizard extends MetricBase {
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
  /** The source of the operation */
  readonly source?: string;
}

export interface BeanstalkOpenApplication extends MetricBase {}

export interface BeanstalkOpenEnvironment extends MetricBase {}

export interface BeanstalkDeleteApplication extends MetricBase {}

export interface BeanstalkDeleteEnvironment extends MetricBase {}

export interface BeanstalkRestartApplication extends MetricBase {}

export interface BeanstalkRebuildEnvironment extends MetricBase {}

export interface BeanstalkEditEnvironment extends MetricBase {}

export interface CloudfrontOpenDistribution extends MetricBase {}

export interface CloudfrontOpenStreamingDistribution extends MetricBase {}

export interface CloudfrontOpenInvalidationRequest extends MetricBase {}

export interface CloudfrontDeleteDistribution extends MetricBase {}

export interface CloudfrontDeleteStreamingDistribution extends MetricBase {}

export interface CloudfrontCreateDistribution extends MetricBase {}

export interface CloudfrontCreateStreamingDistribution extends MetricBase {}

export interface CloudwatchlogsCopyArn extends MetricBase {
  /** CloudWatch Logs entity */
  readonly cloudWatchResourceType: CloudWatchResourceType;
}

export interface CloudwatchlogsOpen extends MetricBase {
  /** CloudWatch Logs entity */
  readonly cloudWatchResourceType: CloudWatchResourceType;
  /** Presentation mode used in a CloudWatch Logs operation */
  readonly cloudWatchLogsPresentation?: CloudWatchLogsPresentation;
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
  /** The source of the operation */
  readonly source: string;
}

export interface CloudwatchlogsOpenGroup extends MetricBase {
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
}

export interface CloudwatchlogsOpenStream extends MetricBase {
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
}

export interface CloudwatchlogsDelete extends MetricBase {
  /** CloudWatch Logs entity */
  readonly cloudWatchResourceType: CloudWatchResourceType;
}

export interface CloudwatchlogsDownload extends MetricBase {
  /** CloudWatch Logs entity */
  readonly cloudWatchResourceType: CloudWatchResourceType;
}

export interface CloudwatchlogsDownloadStreamToFile extends MetricBase {}

export interface CloudwatchlogsOpenStreamInEditor extends MetricBase {}

export interface CloudwatchlogsViewCurrentMessagesInEditor extends MetricBase {}

export interface CloudwatchlogsWrapEvents extends MetricBase {
  /** True if turned on, false if turned off */
  readonly enabled: boolean;
}

export interface CloudwatchlogsTailStream extends MetricBase {
  /** True if turned on, false if turned off */
  readonly enabled: boolean;
}

export interface CloudwatchlogsRefresh extends MetricBase {
  /** CloudWatch Logs entity */
  readonly cloudWatchResourceType: CloudWatchResourceType;
}

export interface CloudwatchlogsRefreshGroup extends MetricBase {}

export interface CloudwatchlogsRefreshStream extends MetricBase {}

export interface CloudwatchlogsFilter extends MetricBase {
  /** CloudWatch Logs entity */
  readonly cloudWatchResourceType: CloudWatchResourceType;
  /** The source of the operation */
  readonly source?: string;
  /** A text based filter was used */
  readonly hasTextFilter?: boolean;
  /** A time based filter was used */
  readonly hasTimeFilter?: boolean;
}

export interface CloudwatchlogsSearchStream extends MetricBase {}

export interface CloudwatchlogsSearchGroup extends MetricBase {}

export interface CloudwatchlogsShowEventsAround extends MetricBase {}

export interface CloudformationCreateProject extends MetricBase {
  /** Generic name of a template */
  readonly templateName: string;
}

export interface CloudformationDeploy extends MetricBase {
  /** Whether or not the deploy targets a new destination (true) or an existing destination (false) */
  readonly initialDeploy: boolean;
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
  /** The source of the operation */
  readonly source?: string;
}

export interface CloudformationPublishWizard extends MetricBase {
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
  /** The source of the operation */
  readonly source?: string;
}

export interface CloudformationOpen extends MetricBase {}

export interface CodecommitCloneRepo extends MetricBase {}

export interface CodecommitCreateRepo extends MetricBase {}

export interface CodecommitSetCredentials extends MetricBase {
  /** The type of credential that was selected */
  readonly credentialType?: CredentialType;
}

export interface DynamodbCreateTable extends MetricBase {}

export interface DynamodbDeleteTable extends MetricBase {}

export interface DynamodbEdit extends MetricBase {
  /** The type of DynamoDB entity referenced by a metric or operation */
  readonly dynamoDbTarget: DynamoDbTarget;
}

export interface DynamodbFetchRecords extends MetricBase {
  /** The type of fetch being performed */
  readonly dynamoDbFetchType: DynamoDbFetchType;
  /** The type of index being hit for the query/scan operation */
  readonly dynamoDbIndexType?: DynamoDbIndexType;
}

export interface DynamodbOpenTable extends MetricBase {}

export interface DynamodbView extends MetricBase {
  /** The type of DynamoDB entity referenced by a metric or operation */
  readonly dynamoDbTarget: DynamoDbTarget;
}

export interface Ec2ChangeState extends MetricBase {
  /** Actions that can affect an EC2 Instance state */
  readonly ec2InstanceState: Ec2InstanceState;
}

export interface Ec2ClearPrivateKey extends MetricBase {}

export interface Ec2ConnectToInstance extends MetricBase {
  /** Ways to connect to an EC2 Instance */
  readonly ec2ConnectionType: Ec2ConnectionType;
}

export interface Ec2CopyAmiToRegion extends MetricBase {}

export interface Ec2CreateAmi extends MetricBase {}

export interface Ec2CreateElasticIp extends MetricBase {}

export interface Ec2CreateKeyPair extends MetricBase {}

export interface Ec2CreateSecurityGroup extends MetricBase {}

export interface Ec2CreateSnapshot extends MetricBase {}

export interface Ec2CreateVolume extends MetricBase {}

export interface Ec2DeleteAmi extends MetricBase {}

export interface Ec2DeleteElasticIp extends MetricBase {}

export interface Ec2DeleteKeyPair extends MetricBase {}

export interface Ec2DeleteSecurityGroup extends MetricBase {}

export interface Ec2DeleteSnapshot extends MetricBase {}

export interface Ec2DeleteVolume extends MetricBase {}

export interface Ec2EditAmiPermission extends MetricBase {}

export interface Ec2EditInstanceElasticIp extends MetricBase {
  /** True if turned on, false if turned off */
  readonly enabled?: boolean;
}

export interface Ec2EditInstanceShutdownBehavior extends MetricBase {}

export interface Ec2EditInstanceTerminationProtection extends MetricBase {
  /** True if turned on, false if turned off */
  readonly enabled?: boolean;
}

export interface Ec2EditInstanceType extends MetricBase {}

export interface Ec2EditInstanceUserData extends MetricBase {}

export interface Ec2EditSecurityGroupPermission extends MetricBase {}

export interface Ec2EditVolumeAttachment extends MetricBase {
  /** True if turned on, false if turned off */
  readonly enabled: boolean;
}

export interface Ec2ExportPrivateKey extends MetricBase {}

export interface Ec2ImportPrivateKey extends MetricBase {}

export interface Ec2LaunchInstance extends MetricBase {}

export interface Ec2OpenInstances extends MetricBase {}

export interface Ec2OpenAMIs extends MetricBase {}

export interface Ec2OpenElasticIPs extends MetricBase {}

export interface Ec2OpenKeyPairs extends MetricBase {}

export interface Ec2OpenSecurityGroups extends MetricBase {}

export interface Ec2OpenVolumes extends MetricBase {}

export interface Ec2ViewInstanceSystemLog extends MetricBase {}

export interface EcsOpenCluster extends MetricBase {}

export interface Ec2ViewInstanceUserData extends MetricBase {}

export interface EcsEnableExecuteCommand extends MetricBase {}

export interface EcsDisableExecuteCommand extends MetricBase {}

export interface EcsRunExecuteCommand extends MetricBase {
  /** Type of execution selected while running the execute command */
  readonly ecsExecuteCommandType: EcsExecuteCommandType;
}

export interface EcrCopyRepositoryUri extends MetricBase {}

export interface EcrCopyTagUri extends MetricBase {}

export interface EcrCreateRepository extends MetricBase {}

export interface EcrDeleteRepository extends MetricBase {}

export interface EcrDeleteTags extends MetricBase {}

export interface EcrDeployImage extends MetricBase {
  /** The source content specified in the ECR deployment request */
  readonly ecrDeploySource?: EcrDeploySource;
}

export interface EcsDeployScheduledTask extends MetricBase {
  /** Infrastructure type used by ECS tasks and services */
  readonly ecsLaunchType: EcsLaunchType;
}

export interface EcsDeployService extends MetricBase {
  /** Infrastructure type used by ECS tasks and services */
  readonly ecsLaunchType: EcsLaunchType;
}

export interface EcsDeployTask extends MetricBase {
  /** Infrastructure type used by ECS tasks and services */
  readonly ecsLaunchType: EcsLaunchType;
}

export interface EcsPublishWizard extends MetricBase {}

export interface EcsOpenRepository extends MetricBase {}

export interface EcsDeleteService extends MetricBase {}

export interface EcsEditService extends MetricBase {}

export interface EcsDeleteCluster extends MetricBase {}

export interface EcsStopTask extends MetricBase {}

export interface EcsDeleteScheduledTask extends MetricBase {}

export interface FeedbackResult extends MetricBase {}

export interface FileEditAwsFile extends MetricBase {
  /** AWS filetype kind */
  readonly awsFiletype: AwsFiletype;
  /** Filename extension (examples: .txt, .yml, .yaml, .asl.yaml, ...), or empty string if the filename does not contain dot (.) between two chars. */
  readonly filenameExt?: string;
}

export interface IamOpenRole extends MetricBase {}

export interface IamOpenGroup extends MetricBase {}

export interface IamOpenUser extends MetricBase {}

export interface IamOpen extends MetricBase {
  /** The type of IAM resource referenced by a metric or operation */
  readonly iamResourceType: IamResourceType;
}

export interface IamCreate extends MetricBase {
  /** The type of IAM resource referenced by a metric or operation */
  readonly iamResourceType: IamResourceType;
}

export interface IamDelete extends MetricBase {
  /** The type of IAM resource referenced by a metric or operation */
  readonly iamResourceType: IamResourceType;
}

export interface IamEdit extends MetricBase {
  /** The type of IAM resource referenced by a metric or operation */
  readonly iamResourceType: IamResourceType;
}

export interface IamCreateUserAccessKey extends MetricBase {}

export interface IamDeleteUserAccessKey extends MetricBase {}

export interface LambdaDelete extends MetricBase {}

export interface LambdaConfigure extends MetricBase {}

export interface LambdaCreate extends MetricBase {
  /** The lambda runtime */
  readonly runtime: Runtime;
}

export interface LambdaCreateProject extends MetricBase {
  /** Language used for the project */
  readonly language: string;
  /** Generic name of a template */
  readonly templateName: string;
  /** A generic variant metadata */
  readonly variant?: string;
}

export interface LambdaGoToHandler extends MetricBase {}

export interface LambdaEditFunction extends MetricBase {
  /** If the operation was an update or not */
  readonly update?: boolean;
  /** The Lambda Package type of the function */
  readonly lambdaPackageType: LambdaPackageType;
}

export interface LambdaInvokeRemote extends MetricBase {
  /** The lambda runtime */
  readonly runtime?: Runtime;
}

export interface LambdaInvokeLocal extends MetricBase {
  /** The lambda runtime */
  readonly runtime?: Runtime;
  /** A generic version metadata */
  readonly version?: string;
  /** The Lambda Package type of the function */
  readonly lambdaPackageType: LambdaPackageType;
  /** If the action was run in debug mode or not */
  readonly debug: boolean;
  /** Lambda architecture identifier */
  readonly lambdaArchitecture?: LambdaArchitecture;
}

export interface LambdaImport extends MetricBase {
  /** The lambda runtime */
  readonly runtime?: Runtime;
}

export interface LambdaUpdateFunctionCode extends MetricBase {
  /** The lambda runtime */
  readonly runtime?: Runtime;
}

export interface LambdaDeploy extends MetricBase {
  /** The Lambda Package type of the function */
  readonly lambdaPackageType: LambdaPackageType;
  /** Whether or not the deploy targets a new destination (true) or an existing destination (false) */
  readonly initialDeploy: boolean;
  /** The lambda runtime */
  readonly runtime?: Runtime;
  /** Language-specific identification. Examples: v4.6.1, netcoreapp3.1, nodejs12.x. Not AWS Lambda specific. Allows for additional details when other fields are opaque, such as the Lambda runtime value 'provided'. */
  readonly platform?: string;
  /** Lambda architecture identifier */
  readonly lambdaArchitecture?: LambdaArchitecture;
  /** Language used for the project */
  readonly language?: string;
  /** Whether or not AWS X-Ray is enabled */
  readonly xrayEnabled?: boolean;
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
  /** The source of the operation */
  readonly source?: string;
}

export interface LambdaPublishWizard extends MetricBase {
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
  /** The source of the operation */
  readonly source?: string;
}

export interface CloudformationDelete extends MetricBase {}

export interface RdsGetCredentials extends MetricBase {
  /** How the database credentials are being retrieved */
  readonly databaseCredentials: DatabaseCredentials;
  /** The database engine used (mysql/postgres/redshift) */
  readonly databaseEngine: string;
}

export interface RdsOpenInstances extends MetricBase {}

export interface RdsOpenSecurityGroups extends MetricBase {}

export interface RdsOpenSubnets extends MetricBase {}

export interface RdsLaunchInstance extends MetricBase {}

export interface RdsCreateSecurityGroup extends MetricBase {}

export interface RdsCreateSubnetGroup extends MetricBase {}

export interface RdsDeleteInstance extends MetricBase {}

export interface RdsDeleteSecurityGroup extends MetricBase {}

export interface RdsDeleteSubnetGroup extends MetricBase {}

export interface RdsCreateConnectionConfiguration extends MetricBase {
  /** How the database credentials are being retrieved */
  readonly databaseCredentials: DatabaseCredentials;
  /** The database engine used (mysql/postgres/redshift) */
  readonly databaseEngine?: string;
}

export interface RedshiftGetCredentials extends MetricBase {
  /** How the database credentials are being retrieved */
  readonly databaseCredentials: DatabaseCredentials;
}

export interface RedshiftCreateConnectionConfiguration extends MetricBase {
  /** How the database credentials are being retrieved */
  readonly databaseCredentials: DatabaseCredentials;
}

export interface SamDeploy extends MetricBase {
  /** A generic version metadata */
  readonly version?: string;
}

export interface SamSync extends MetricBase {
  /** Describes which parts of an application (that we know of) were synced to the cloud. "Code" resources follow the SAM spec: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-sync.html */
  readonly syncedResources: SyncedResources;
  /** The Lambda Package type of the function */
  readonly lambdaPackageType: LambdaPackageType;
  /** A generic version metadata */
  readonly version?: string;
}

export interface SamInit extends MetricBase {
  /** The lambda runtime */
  readonly runtime?: Runtime;
  /** Generic name of a template */
  readonly templateName?: string;
  /** A generic version metadata */
  readonly version?: string;
  /** The Lambda Package type of the function */
  readonly lambdaPackageType?: LambdaPackageType;
  /** The name of the EventBridge Schema used in the operation */
  readonly eventBridgeSchema?: string;
  /** Lambda architecture identifier */
  readonly lambdaArchitecture?: LambdaArchitecture;
}

export interface SchemasView extends MetricBase {}

export interface SchemasDownload extends MetricBase {
  /** Languages targeted by the schemas service */
  readonly schemaLanguage?: SchemaLanguage;
}

export interface SchemasSearch extends MetricBase {}

export interface SessionStart extends MetricBase {}

export interface SessionEnd extends MetricBase {}

export interface S3CopyBucketName extends MetricBase {}

export interface S3CopyPath extends MetricBase {}

export interface S3CopyUri extends MetricBase {}

export interface S3CopyUrl extends MetricBase {
  /** Whether or not it was a presigned request */
  readonly presigned: boolean;
}

export interface S3CreateBucket extends MetricBase {}

export interface S3DeleteBucket extends MetricBase {}

export interface S3DeleteObject extends MetricBase {
  /** The number of successful operations */
  readonly successCount?: number;
  /** The number of failed operations */
  readonly failedCount?: number;
}

export interface S3CreateFolder extends MetricBase {}

export interface S3DownloadObject extends MetricBase {
  /** The number of successful operations */
  readonly successCount?: number;
  /** The number of failed operations */
  readonly failedCount?: number;
  /** The IDE or OS component used for the action. (Examples: S3 download to filesystem, S3 upload from editor, ...) */
  readonly component?: Component;
}

export interface S3DownloadObjects extends MetricBase {}

export interface S3UploadObject extends MetricBase {
  /** The number of successful operations */
  readonly successCount?: number;
  /** The number of failed operations */
  readonly failedCount?: number;
  /** The IDE or OS component used for the action. (Examples: S3 download to filesystem, S3 upload from editor, ...) */
  readonly component?: Component;
}

export interface S3RenameObject extends MetricBase {}

export interface S3UploadObjects extends MetricBase {}

export interface S3OpenEditor extends MetricBase {}

export interface S3EditObject extends MetricBase {
  /** The IDE or OS component used for the action. (Examples: S3 download to filesystem, S3 upload from editor, ...) */
  readonly component?: Component;
}

export interface S3OpenBucketProperties extends MetricBase {}

export interface S3OpenMultipartUpload extends MetricBase {}

export interface ToolkitInit extends MetricBase {}

export interface ToolkitViewLogs extends MetricBase {}

export interface SqsOpenQueue extends MetricBase {
  /** The type of an SQS Queue */
  readonly sqsQueueType: SqsQueueType;
}

export interface SqsCreateQueue extends MetricBase {
  /** The type of an SQS Queue */
  readonly sqsQueueType?: SqsQueueType;
}

export interface SqsSendMessage extends MetricBase {
  /** The type of an SQS Queue */
  readonly sqsQueueType: SqsQueueType;
}

export interface SqsDeleteMessages extends MetricBase {
  /** The type of an SQS Queue */
  readonly sqsQueueType: SqsQueueType;
}

export interface SqsSubscribeSns extends MetricBase {
  /** The type of an SQS Queue */
  readonly sqsQueueType: SqsQueueType;
}

export interface SqsConfigureLambdaTrigger extends MetricBase {
  /** The type of an SQS Queue */
  readonly sqsQueueType: SqsQueueType;
}

export interface SqsEditQueueParameters extends MetricBase {
  /** The type of an SQS Queue */
  readonly sqsQueueType: SqsQueueType;
}

export interface SqsPurgeQueue extends MetricBase {
  /** The type of an SQS Queue */
  readonly sqsQueueType: SqsQueueType;
}

export interface SqsDeleteQueue extends MetricBase {
  /** The type of an SQS Queue */
  readonly sqsQueueType?: SqsQueueType;
}

export interface SnsCreateTopic extends MetricBase {}

export interface SnsCreateSubscription extends MetricBase {}

export interface SnsOpenTopic extends MetricBase {}

export interface SnsOpenSubscriptions extends MetricBase {}

export interface SnsDeleteTopic extends MetricBase {}

export interface SnsDeleteSubscription extends MetricBase {}

export interface SnsPublishMessage extends MetricBase {}

export interface VpcOpenRouteTables extends MetricBase {}

export interface VpcOpenGateways extends MetricBase {}

export interface VpcOpenACLs extends MetricBase {}

export interface VpcOpenSubnets extends MetricBase {}

export interface VpcOpenVPCs extends MetricBase {}

export interface CloudwatchinsightsOpenEditor extends MetricBase {
  /** Dialog open trigger source location */
  readonly insightsDialogOpenSource: InsightsDialogOpenSource;
}

export interface CloudwatchinsightsExecuteQuery extends MetricBase {
  /** User-selected time range type while starting an insights query */
  readonly insightsQueryTimeType: InsightsQueryTimeType;
  /** User-specified search string type while starting an insights query */
  readonly insightsQueryStringType: InsightsQueryStringType;
}

export interface CloudwatchinsightsSaveQuery extends MetricBase {}

export interface CloudwatchinsightsRetrieveQuery extends MetricBase {}

export interface CloudwatchinsightsOpenDetailedLogRecord extends MetricBase {}

export interface ToolkitGetExternalResource extends MetricBase {
  /** The url associated with a metric */
  readonly url: string;
}

export interface DynamicresourceGetResource extends MetricBase {
  /** The dynamic resource type being interacted with */
  readonly resourceType: string;
}

export interface DynamicresourceListResource extends MetricBase {
  /** The dynamic resource type being interacted with */
  readonly resourceType: string;
}

export interface DynamicresourceSelectResources extends MetricBase {}

export interface DynamicresourceCopyIdentifier extends MetricBase {
  /** The dynamic resource type being interacted with */
  readonly resourceType: string;
}

export interface DynamicresourceMutateResource extends MetricBase {
  /** The dynamic resource type being interacted with */
  readonly resourceType: string;
  /** The dynamic resource operation being executed */
  readonly dynamicResourceOperation: DynamicResourceOperation;
}

export interface AwsExperimentActivation extends MetricBase {
  /** The id of the experiment being activated or deactivated */
  readonly experimentId: string;
  /** The experiment action taken action taken */
  readonly experimentState: ExperimentState;
}

export interface AwsToolInstallation extends MetricBase {
  /** The tool being installed */
  readonly toolId: ToolId;
}

export interface AwsModifySetting extends MetricBase {
  /** The id of the setting being changed. Consistent namespace should be used for the id, e.g. codewhisperer_autoSuggestionActivation */
  readonly settingId: string;
  /** The state of the setting being changed to. This should not be recorded for free-form settings like file-system paths. Instead, stick to things like flags, numbers, and enums. */
  readonly settingState?: string;
}

export interface UiClick extends MetricBase {
  /** An identifier associated with a UI element */
  readonly elementId: string;
}

export interface DeeplinkOpen extends MetricBase {
  /** The source of the operation */
  readonly source: string;
  /** The name of the AWS service acted on. These values come from the AWS SDK. To find them in the JAVA SDK search for SERVICE_NAME in each service client, or look for serviceId in metadata in the service2.json */
  readonly serviceType?: string;
}

export interface CodewhispererCodePercentage extends MetricBase {
  /** The metrics accepted on suggested CodeWhisperer code */
  readonly codewhispererAcceptedTokens: number;
  /** Programming language of the CodeWhisperer recommendation */
  readonly codewhispererLanguage: CodewhispererLanguage;
  /** The percentage of acceptance on suggested CodeWhisperer code on the overall code */
  readonly codewhispererPercentage: number;
  /** The metrics generated by the user and acceptance of suggested CodeWhisperer code in the language CodeWhisperer supports. */
  readonly codewhispererTotalTokens: number;
  /** The number of successful operations */
  readonly successCount: number;
}

export interface CodewhispererSecurityScan extends MetricBase {
  /** How many lines of code being sent for security scan */
  readonly codewhispererCodeScanLines: number;
  /** The ID of the security scan job */
  readonly codewhispererCodeScanJobId?: string;
  /** The total size in bytes of customer project to perform security scan on */
  readonly codewhispererCodeScanProjectBytes?: number;
  /** The uncompressed payload size in bytes of the source files in customer project context sent for security scan */
  readonly codewhispererCodeScanSrcPayloadBytes: number;
  /** The uncompressed payload size in bytes of the build files in customer project context sent for security scan */
  readonly codewhispererCodeScanBuildPayloadBytes?: number;
  /** The compressed payload size of source files in bytes of customer project context sent for security scan */
  readonly codewhispererCodeScanSrcZipFileBytes: number;
  /** The compressed payload size of built jars in bytes of customer project context sent for security scan. This is only applicable for Java project */
  readonly codewhispererCodeScanBuildZipFileBytes?: number;
  /** The number of security issues been detected */
  readonly codewhispererCodeScanTotalIssues: number;
  /** Programming language of the CodeWhisperer recommendation */
  readonly codewhispererLanguage: CodewhispererLanguage;
  /** Time taken for context truncation in milliseconds */
  readonly contextTruncationDuration: number;
  /** Time taken to fetch the upload URL and upload the artifacts in milliseconds */
  readonly artifactsUploadDuration: number;
  /** Time taken to invoke code scan service APIs in milliseconds */
  readonly codeScanServiceInvocationsDuration: number;
  /** The start URL of current SSO connection */
  readonly credentialStartUrl?: string;
}

export interface CodewhispererServiceInvocation extends MetricBase {
  /** The type of the Automated trigger to send request to CodeWhisperer service */
  readonly codewhispererAutomatedTriggerType?: CodewhispererAutomatedTriggerType;
  /** Completion Type of the inference results returned from CodeWhisperer model layer */
  readonly codewhispererCompletionType?: CodewhispererCompletionType;
  /** cursor location offset in the editor when invoking CodeWhisperer for recommendation */
  readonly codewhispererCursorOffset: number;
  /** Programming language of the CodeWhisperer recommendation */
  readonly codewhispererLanguage: CodewhispererLanguage;
  /** The last index of recommendation from a particular response */
  readonly codewhispererLastSuggestionIndex?: number;
  /** The line number of the cursor when the event happens */
  readonly codewhispererLineNumber: number;
  /** The ID of the request to CodeWhisperer service */
  readonly codewhispererRequestId?: string;
  /** the pre-defined set of values for runtime version of the language of CodeWhisperer recommendation */
  readonly codewhispererRuntime?: CodewhispererRuntime;
  /** the original (free-text) of the runtime version of the language of CodeWhisperer recommendation */
  readonly codewhispererRuntimeSource?: string;
  /** The unique identifier for a CodeWhisperer session(which can contain multiple requests) */
  readonly codewhispererSessionId?: string;
  /** The type of the user trigger to send request to CodeWhisperer service */
  readonly codewhispererTriggerType: CodewhispererTriggerType;
  /** The start URL of current SSO connection */
  readonly credentialStartUrl?: string;
  /** The active cell index where the invocation to CodeWhisperer happens */
  readonly codewhispererJupyterLabCellIndex?: number;
  /** The total number of cells in the jupyter lab editor when the CodeWhisperer invocation happens */
  readonly codewhispererJupyterLabCellCount?: number;
  /** The type of the cell where the invocation to CodeWhisperer happens  */
  readonly codewhispererJupyterLabCellType?: CodewhispererJupyterLabCellType;
}

export interface CodewhispererBlockedInvocation extends MetricBase {
  /** The type of the Automated trigger to send request to CodeWhisperer service */
  readonly codewhispererAutomatedTriggerType?: CodewhispererAutomatedTriggerType;
  /** cursor location offset in the editor when invoking CodeWhisperer for recommendation */
  readonly codewhispererCursorOffset: number;
  /** Programming language of the CodeWhisperer recommendation */
  readonly codewhispererLanguage: CodewhispererLanguage;
  /** The line number of the cursor when the event happens */
  readonly codewhispererLineNumber: number;
  /** The type of the user trigger to send request to CodeWhisperer service */
  readonly codewhispererTriggerType: CodewhispererTriggerType;
  /** The start URL of current SSO connection */
  readonly credentialStartUrl?: string;
}

export interface CodewhispererUserDecision extends MetricBase {
  /** Completion Type of the inference results returned from CodeWhisperer model layer */
  readonly codewhispererCompletionType: CodewhispererCompletionType;
  /** Programming language of the CodeWhisperer recommendation */
  readonly codewhispererLanguage: CodewhispererLanguage;
  /** The number of recommendations received so far when user makes a decision */
  readonly codewhispererPaginationProgress?: number;
  /** The ID of the request to CodeWhisperer service */
  readonly codewhispererRequestId: string;
  /** the pre-defined set of values for runtime version of the language of CodeWhisperer recommendation */
  readonly codewhispererRuntime?: CodewhispererRuntime;
  /** the original (free-text) of the runtime version of the language of CodeWhisperer recommendation */
  readonly codewhispererRuntimeSource?: string;
  /** The unique identifier for a CodeWhisperer session(which can contain multiple requests) */
  readonly codewhispererSessionId?: string;
  /** The index for each suggestion, respectively, in the list of suggestions returned from service invocation */
  readonly codewhispererSuggestionIndex: number;
  /** Number of references the particular suggestion is referenced with. */
  readonly codewhispererSuggestionReferenceCount: number;
  /** The list of unique license names for a particular suggestion */
  readonly codewhispererSuggestionReferences?: string;
  /** The number of import statements included with recommendation. */
  readonly codewhispererSuggestionImportCount?: number;
  /** User decision of each of the suggestion returned from CodeWhisperer */
  readonly codewhispererSuggestionState: CodewhispererSuggestionState;
  /** The type of the user trigger to send request to CodeWhisperer service */
  readonly codewhispererTriggerType: CodewhispererTriggerType;
  /** The start URL of current SSO connection */
  readonly credentialStartUrl?: string;
}

export interface CodewhispererUserTriggerDecision extends MetricBase {
  /** The unique identifier for a CodeWhisperer session(which can contain multiple requests) */
  readonly codewhispererSessionId?: string;
  /** The request id of the first request in a paginated session. */
  readonly codewhispererFirstRequestId: string;
  /** The start URL of current SSO connection */
  readonly credentialStartUrl?: string;
  /** If user has accepted only part of the recommendation or not. */
  readonly codewhispererIsPartialAcceptance?: boolean;
  /** The number of times the user accept part of the recommendations. */
  readonly codewhispererPartialAcceptanceCount?: number;
  /** The number of characters user has accepted through partial acceptance. */
  readonly codewhispererCharactersAccepted?: number;
  /** The number of characters originally recommended to the user in partial acceptance scenario. */
  readonly codewhispererCharactersRecommended?: number;
  /** Completion Type of the inference results returned from CodeWhisperer model layer */
  readonly codewhispererCompletionType: CodewhispererCompletionType;
  /** Programming language of the CodeWhisperer recommendation */
  readonly codewhispererLanguage: CodewhispererLanguage;
  /** The type of the user trigger to send request to CodeWhisperer service */
  readonly codewhispererTriggerType: CodewhispererTriggerType;
  /** The type of the Automated trigger to send request to CodeWhisperer service */
  readonly codewhispererAutomatedTriggerType?: CodewhispererAutomatedTriggerType;
  /** The line number of the cursor when the event happens */
  readonly codewhispererLineNumber: number;
  /** cursor location offset in the editor when invoking CodeWhisperer for recommendation */
  readonly codewhispererCursorOffset: number;
  /** The total number of code suggestions in a paginated session. */
  readonly codewhispererSuggestionCount: number;
  /** The number of import statements included with recommendation. */
  readonly codewhispererSuggestionImportCount: number;
  /** The time that recommendations are shown to the user in a paginated session. */
  readonly codewhispererTotalShownTime?: number;
  /** The character that triggered recommendation for special characters trigger. */
  readonly codewhispererTriggerCharacter?: string;
  /** The length of additional characters inputted by the user since the invocation. */
  readonly codewhispererTypeaheadLength: number;
  /** The time from last document change to the current document change. */
  readonly codewhispererTimeSinceLastDocumentChange?: number;
  /** The time from last user decision to current invocation. */
  readonly codewhispererTimeSinceLastUserDecision?: number;
  /** The time from user trigger to the first recommendation is received. */
  readonly codewhispererTimeToFirstRecommendation?: number;
  /** The aggregated user decision from previous trigger. */
  readonly codewhispererPreviousSuggestionState?: CodewhispererPreviousSuggestionState;
  /** User decision of each of the suggestion returned from CodeWhisperer */
  readonly codewhispererSuggestionState: CodewhispererSuggestionState;
  /** The result from Classifier trigger. */
  readonly codewhispererClassifierResult?: number;
  /** The active cell index where the invocation to CodeWhisperer happens */
  readonly codewhispererJupyterLabCellIndex?: number;
  /** The total number of cells in the jupyter lab editor when the CodeWhisperer invocation happens */
  readonly codewhispererJupyterLabCellCount?: number;
  /** The type of the cell where the invocation to CodeWhisperer happens  */
  readonly codewhispererJupyterLabCellType?: CodewhispererJupyterLabCellType;
}

export interface CodewhispererUserModification extends MetricBase {
  /** Completion Type of the inference results returned from CodeWhisperer model layer */
  readonly codewhispererCompletionType: CodewhispererCompletionType;
  /** Programming language of the CodeWhisperer recommendation */
  readonly codewhispererLanguage: CodewhispererLanguage;
  /** The percentage of user modifications on the suggested code */
  readonly codewhispererModificationPercentage: number;
  /** The ID of the request to CodeWhisperer service */
  readonly codewhispererRequestId: string;
  /** the pre-defined set of values for runtime version of the language of CodeWhisperer recommendation */
  readonly codewhispererRuntime?: CodewhispererRuntime;
  /** the original (free-text) of the runtime version of the language of CodeWhisperer recommendation */
  readonly codewhispererRuntimeSource?: string;
  /** The unique identifier for a CodeWhisperer session(which can contain multiple requests) */
  readonly codewhispererSessionId?: string;
  /** The index for each suggestion, respectively, in the list of suggestions returned from service invocation */
  readonly codewhispererSuggestionIndex: number;
  /** The type of the user trigger to send request to CodeWhisperer service */
  readonly codewhispererTriggerType: CodewhispererTriggerType;
  /** The start URL of current SSO connection */
  readonly credentialStartUrl?: string;
}

export interface CodewhispererPerceivedLatency extends MetricBase {
  /** The ID of the request to CodeWhisperer service */
  readonly codewhispererRequestId: string;
  /** The unique identifier for a CodeWhisperer session(which can contain multiple requests) */
  readonly codewhispererSessionId?: string;
  /** The type of the user trigger to send request to CodeWhisperer service */
  readonly codewhispererTriggerType: CodewhispererTriggerType;
  /** Completion Type of the inference results returned from CodeWhisperer model layer */
  readonly codewhispererCompletionType: CodewhispererCompletionType;
  /** Programming language of the CodeWhisperer recommendation */
  readonly codewhispererLanguage: CodewhispererLanguage;
  /** The start URL of current SSO connection */
  readonly credentialStartUrl?: string;
}

export interface CodewhispererClientComponentLatency extends MetricBase {
  /** The ID of the request to CodeWhisperer service */
  readonly codewhispererRequestId: string;
  /** The unique identifier for a CodeWhisperer session(which can contain multiple requests) */
  readonly codewhispererSessionId: string;
  /** The time it takes for the plugin to make the first GenerateCompletions API call after the user performs the CW trigger action. */
  readonly codewhispererPreprocessingLatency: number;
  /** The time it takes to get the Sono/SSO credential for the invocation. */
  readonly codewhispererCredentialFetchingLatency: number;
  /** The time it takes for the first completions to be displayed in the IDE after the plugin receives the initial Completions object. */
  readonly codewhispererPostprocessingLatency: number;
  /** The time it takes for the response to be received after the plugin makes a first GenerateCompletions API call. */
  readonly codewhispererFirstCompletionLatency: number;
  /** The time it takes for the first completion to be shown in the IDE after the user performs the CW trigger action. */
  readonly codewhispererEndToEndLatency: number;
  /** The time it takes for the last GenerateCompletions response to be received after plugin makes a first call to GenerateCompletions API. */
  readonly codewhispererAllCompletionsLatency: number;
  /** Completion Type of the inference results returned from CodeWhisperer model layer */
  readonly codewhispererCompletionType: CodewhispererCompletionType;
  /** The type of the user trigger to send request to CodeWhisperer service */
  readonly codewhispererTriggerType: CodewhispererTriggerType;
  /** Programming language of the CodeWhisperer recommendation */
  readonly codewhispererLanguage: CodewhispererLanguage;
  /** The start URL of current SSO connection */
  readonly credentialStartUrl?: string;
}

export interface CodecatalystCreateDevEnvironment extends MetricBase {
  /** Opaque AWS Builder ID identifier */
  readonly userId: string;
  /** Type of Git repository provided to the Amazon CodeCatalyst dev environment create wizard */
  readonly codecatalyst_createDevEnvironmentRepoType?: Codecatalyst_createDevEnvironmentRepoType;
}

export interface CodecatalystUpdateDevEnvironmentSettings extends MetricBase {
  /** Opaque AWS Builder ID identifier */
  readonly userId: string;
  /** Locality of the Amazon CodeCatalyst update dev environment request (i.e., from the thin client or the local IDE instance) */
  readonly codecatalyst_updateDevEnvironmentLocationType: Codecatalyst_updateDevEnvironmentLocationType;
}

export interface CodecatalystUpdateDevfile extends MetricBase {
  /** Opaque AWS Builder ID identifier */
  readonly userId: string;
}

export interface CodecatalystLocalClone extends MetricBase {
  /** Opaque AWS Builder ID identifier */
  readonly userId: string;
}

export interface CodecatalystConnect extends MetricBase {
  /** Opaque AWS Builder ID identifier */
  readonly userId: string;
}

export interface CodecatalystDevEnvironmentWorkflowStatistic
  extends MetricBase {
  /** Opaque AWS Builder ID identifier */
  readonly userId: string;
  /** Workflow step name */
  readonly codecatalyst_devEnvironmentWorkflowStep: string;
  /** Workflow error name */
  readonly codecatalyst_devEnvironmentWorkflowError?: string;
}

export interface VscodeExecuteCommand extends MetricBase {
  /** The id of a VS Code command */
  readonly command: string;
  /** Number of times the telemetry event was debounced before emission */
  readonly debounceCount: number;
}

export interface SsmCreateDocument extends MetricBase {
  /** SSM Create document format selection */
  readonly documentFormat?: DocumentFormat;
  /** Starter template chosen during create document */
  readonly starterTemplate?: string;
}

export interface SsmDeleteDocument extends MetricBase {}

export interface SsmExecuteDocument extends MetricBase {}

export interface SsmOpenDocument extends MetricBase {}

export interface SsmPublishDocument extends MetricBase {
  /** SSM Publish Document operation type */
  readonly ssmOperation: SsmOperation;
}

export interface SsmUpdateDocumentVersion extends MetricBase {}

export interface StepfunctionsCreateStateMachineFromTemplate
  extends MetricBase {}

export interface StepfunctionsDownloadStateMachineDefinition
  extends MetricBase {}

export interface StepfunctionsExecuteStateMachine extends MetricBase {}

export interface StepfunctionsExecuteStateMachineView extends MetricBase {}

export interface StepfunctionsPreviewstatemachine extends MetricBase {}

export interface VscodeActiveRegions extends MetricBase {}

export interface VscodeViewLogs extends MetricBase {}

export interface AwsShowExplorerErrorDetails extends MetricBase {}

export interface AwsShowRegion extends MetricBase {}

export interface AwsHideRegion extends MetricBase {}

export interface SamDetect extends MetricBase {}

export interface CdkExplorerDisabled extends MetricBase {}

export interface CdkExplorerEnabled extends MetricBase {}

export interface CdkAppExpanded extends MetricBase {}

export interface CdkProvideFeedback extends MetricBase {}

export interface CdkHelp extends MetricBase {}

export interface CdkRefreshExplorer extends MetricBase {}

export interface SamAttachDebugger extends MetricBase {
  /** The Lambda Package type of the function */
  readonly lambdaPackageType: LambdaPackageType;
  /** The lambda runtime */
  readonly runtime: Runtime;
  /** A generic number of attempts */
  readonly attempts: number;
  /** Lambda architecture identifier */
  readonly lambdaArchitecture?: LambdaArchitecture;
}

export interface SamOpenConfigUi extends MetricBase {}

export type Result = "Succeeded" | "Failed" | "Cancelled";
export type Runtime =
  | "dotnetcore3.1"
  | "dotnetcore2.1"
  | "dotnet5.0"
  | "dotnet6"
  | "dotnet7"
  | "nodejs18.x"
  | "nodejs16.x"
  | "nodejs14.x"
  | "nodejs12.x"
  | "nodejs10.x"
  | "nodejs8.10"
  | "ruby2.5"
  | "java8"
  | "java8.al2"
  | "java11"
  | "go1.x"
  | "python3.9"
  | "python3.8"
  | "python3.7"
  | "python3.6"
  | "python2.7";
export type LambdaArchitecture = "x86_64" | "arm64";
export type AppRunnerServiceSource = "ecr" | "ecrPublic" | "repository";
export type AppRunnerServiceStatus =
  | "CREATE_FAILED"
  | "RUNNING"
  | "DELETED"
  | "DELETE_FAILED"
  | "PAUSED"
  | "OPERATION_IN_PROGRESS";
export type CredentialType =
  | "staticProfile"
  | "staticSessionProfile"
  | "credentialProcessProfile"
  | "assumeRoleProfile"
  | "assumeMfaRoleProfile"
  | "assumeSamlRoleProfile"
  | "ssoProfile"
  | "ecsMetatdata"
  | "ec2Metadata"
  | "bearerToken"
  | "other";
export type CredentialSourceId =
  | "sharedCredentials"
  | "sdkStore"
  | "ec2"
  | "ecs"
  | "envVars"
  | "awsId"
  | "iamIdentityCenter"
  | "other";
export type CredentialModification = "Add" | "Edit" | "Delete";
export type CloudWatchResourceType = "logGroup" | "logGroupList" | "logStream";
export type CloudWatchLogsPresentation = "ui" | "text";
export type DynamoDbTarget = "table" | "tableProperties" | "tableStream";
export type DynamoDbFetchType = "scan" | "query";
export type DynamoDbIndexType =
  | "primary"
  | "localSecondary"
  | "globalSecondary";
export type Ec2InstanceState = "start" | "stop" | "reboot" | "terminate";
export type Ec2ConnectionType = "remoteDesktop" | "ssh" | "scp";
export type EcsExecuteCommandType = "command" | "shell";
export type EcrDeploySource = "dockerfile" | "tag";
export type EcsLaunchType = "ec2" | "fargate";
export type AwsFiletype =
  | "awsCredentials"
  | "cloudformation"
  | "cloudformationSam"
  | "codebuildBuildspec"
  | "ecsTask"
  | "eventbridgeSchema"
  | "iamPolicy"
  | "samconfig"
  | "serverless"
  | "stepfunctionsAsl"
  | "smithyModel"
  | "ssmDocument"
  | "other";
export type IamResourceType = "group" | "role" | "user";
export type LambdaPackageType = "Zip" | "Image";
export type DatabaseCredentials = "IAM" | "SecretsManager";
export type SyncedResources = "AllResources" | "CodeOnly";
export type SchemaLanguage = "Java8" | "Python36" | "TypeScript3";
export type Component = "editor" | "viewer" | "filesystem";
export type SqsQueueType = "standard" | "fifo";
export type InsightsDialogOpenSource =
  | "explorer"
  | "resultsWindow"
  | "logGroup";
export type InsightsQueryTimeType = "relative" | "absolute";
export type InsightsQueryStringType = "insights" | "searchTerm";
export type DynamicResourceOperation = "Create" | "Update" | "Delete";
export type ExperimentState = "activated" | "deactivated";
export type ToolId =
  | "session-manager-plugin"
  | "dotnet-lambda-deploy"
  | "dotnet-deploy-cli"
  | "aws-cli"
  | "sam-cli";
export type CodewhispererLanguage =
  | "java"
  | "python"
  | "javascript"
  | "plaintext"
  | "jsx"
  | "typescript"
  | "tsx"
  | "csharp"
  | "c"
  | "cpp"
  | "go"
  | "kotlin"
  | "php"
  | "ruby"
  | "rust"
  | "scala"
  | "shell"
  | "sql"
  | "ipynb";
export type CodewhispererAutomatedTriggerType =
  | "KeyStrokeCount"
  | "SpecialCharacters"
  | "Enter"
  | "IntelliSenseAcceptance"
  | "IdleTime"
  | "Classifier"
  | "NewCell";
export type CodewhispererCompletionType = "Line" | "Block";
export type CodewhispererRuntime =
  | "java8"
  | "java11"
  | "java16"
  | "python2"
  | "python3"
  | "javascript"
  | "unknown";
export type CodewhispererTriggerType = "OnDemand" | "AutoTrigger";
export type CodewhispererJupyterLabCellType = 'code' | 'markdown' | 'raw';
export type CodewhispererSuggestionState =
  | "Accept"
  | "Reject"
  | "Discard"
  | "Ignore"
  | "Filter"
  | "Unseen"
  | "Empty";
export type CodewhispererPreviousSuggestionState =
  | "Accept"
  | "Reject"
  | "Discard"
  | "Empty";
export type Codecatalyst_createDevEnvironmentRepoType =
  | "linked"
  | "unlinked"
  | "none";
export type Codecatalyst_updateDevEnvironmentLocationType = "remote" | "local";
export type DocumentFormat = "JSON, YAML";
export type SsmOperation = "Create" | "Update";

export interface MetricDefinition {
  readonly unit: string;
  readonly passive: boolean;
  readonly requiredMetadata: readonly string[];
}

export interface MetricShapes {
  readonly apigateway_copyUrl: ApigatewayCopyUrl;
  readonly apigateway_invokeLocal: ApigatewayInvokeLocal;
  readonly apigateway_invokeRemote: ApigatewayInvokeRemote;
  readonly apigateway_startLocalServer: ApigatewayStartLocalServer;
  readonly apprunner_openServiceUrl: ApprunnerOpenServiceUrl;
  readonly apprunner_copyServiceUrl: ApprunnerCopyServiceUrl;
  readonly apprunner_createService: ApprunnerCreateService;
  readonly apprunner_pauseService: ApprunnerPauseService;
  readonly apprunner_resumeService: ApprunnerResumeService;
  readonly apprunner_deleteService: ApprunnerDeleteService;
  readonly apprunner_startDeployment: ApprunnerStartDeployment;
  readonly apprunner_viewApplicationLogs: ApprunnerViewApplicationLogs;
  readonly apprunner_viewServiceLogs: ApprunnerViewServiceLogs;
  readonly aws_copyArn: AwsCopyArn;
  readonly aws_deleteResource: AwsDeleteResource;
  readonly aws_setCredentials: AwsSetCredentials;
  readonly aws_setRegion: AwsSetRegion;
  readonly aws_setPartition: AwsSetPartition;
  readonly aws_openCredentials: AwsOpenCredentials;
  readonly aws_openUrl: AwsOpenUrl;
  readonly aws_saveCredentials: AwsSaveCredentials;
  readonly aws_modifyCredentials: AwsModifyCredentials;
  readonly aws_loadCredentials: AwsLoadCredentials;
  readonly aws_createCredentials: AwsCreateCredentials;
  readonly aws_injectCredentials: AwsInjectCredentials;
  readonly aws_validateCredentials: AwsValidateCredentials;
  readonly aws_refreshCredentials: AwsRefreshCredentials;
  readonly aws_loginWithBrowser: AwsLoginWithBrowser;
  readonly aws_help: AwsHelp;
  readonly aws_helpQuickstart: AwsHelpQuickstart;
  readonly aws_showExtensionSource: AwsShowExtensionSource;
  readonly aws_refreshExplorer: AwsRefreshExplorer;
  readonly aws_expandExplorerNode: AwsExpandExplorerNode;
  readonly aws_reportPluginIssue: AwsReportPluginIssue;
  readonly beanstalk_deploy: BeanstalkDeploy;
  readonly beanstalk_publishWizard: BeanstalkPublishWizard;
  readonly beanstalk_openApplication: BeanstalkOpenApplication;
  readonly beanstalk_openEnvironment: BeanstalkOpenEnvironment;
  readonly beanstalk_deleteApplication: BeanstalkDeleteApplication;
  readonly beanstalk_deleteEnvironment: BeanstalkDeleteEnvironment;
  readonly beanstalk_restartApplication: BeanstalkRestartApplication;
  readonly beanstalk_rebuildEnvironment: BeanstalkRebuildEnvironment;
  readonly beanstalk_editEnvironment: BeanstalkEditEnvironment;
  readonly cloudfront_openDistribution: CloudfrontOpenDistribution;
  readonly cloudfront_openStreamingDistribution: CloudfrontOpenStreamingDistribution;
  readonly cloudfront_openInvalidationRequest: CloudfrontOpenInvalidationRequest;
  readonly cloudfront_deleteDistribution: CloudfrontDeleteDistribution;
  readonly cloudfront_deleteStreamingDistribution: CloudfrontDeleteStreamingDistribution;
  readonly cloudfront_createDistribution: CloudfrontCreateDistribution;
  readonly cloudfront_createStreamingDistribution: CloudfrontCreateStreamingDistribution;
  readonly cloudwatchlogs_copyArn: CloudwatchlogsCopyArn;
  readonly cloudwatchlogs_open: CloudwatchlogsOpen;
  readonly cloudwatchlogs_openGroup: CloudwatchlogsOpenGroup;
  readonly cloudwatchlogs_openStream: CloudwatchlogsOpenStream;
  readonly cloudwatchlogs_delete: CloudwatchlogsDelete;
  readonly cloudwatchlogs_download: CloudwatchlogsDownload;
  readonly cloudwatchlogs_downloadStreamToFile: CloudwatchlogsDownloadStreamToFile;
  readonly cloudwatchlogs_openStreamInEditor: CloudwatchlogsOpenStreamInEditor;
  readonly cloudwatchlogs_viewCurrentMessagesInEditor: CloudwatchlogsViewCurrentMessagesInEditor;
  readonly cloudwatchlogs_wrapEvents: CloudwatchlogsWrapEvents;
  readonly cloudwatchlogs_tailStream: CloudwatchlogsTailStream;
  readonly cloudwatchlogs_refresh: CloudwatchlogsRefresh;
  readonly cloudwatchlogs_refreshGroup: CloudwatchlogsRefreshGroup;
  readonly cloudwatchlogs_refreshStream: CloudwatchlogsRefreshStream;
  readonly cloudwatchlogs_filter: CloudwatchlogsFilter;
  readonly cloudwatchlogs_searchStream: CloudwatchlogsSearchStream;
  readonly cloudwatchlogs_searchGroup: CloudwatchlogsSearchGroup;
  readonly cloudwatchlogs_showEventsAround: CloudwatchlogsShowEventsAround;
  readonly cloudformation_createProject: CloudformationCreateProject;
  readonly cloudformation_deploy: CloudformationDeploy;
  readonly cloudformation_publishWizard: CloudformationPublishWizard;
  readonly cloudformation_open: CloudformationOpen;
  readonly codecommit_cloneRepo: CodecommitCloneRepo;
  readonly codecommit_createRepo: CodecommitCreateRepo;
  readonly codecommit_setCredentials: CodecommitSetCredentials;
  readonly dynamodb_createTable: DynamodbCreateTable;
  readonly dynamodb_deleteTable: DynamodbDeleteTable;
  readonly dynamodb_edit: DynamodbEdit;
  readonly dynamodb_fetchRecords: DynamodbFetchRecords;
  readonly dynamodb_openTable: DynamodbOpenTable;
  readonly dynamodb_view: DynamodbView;
  readonly ec2_changeState: Ec2ChangeState;
  readonly ec2_clearPrivateKey: Ec2ClearPrivateKey;
  readonly ec2_connectToInstance: Ec2ConnectToInstance;
  readonly ec2_copyAmiToRegion: Ec2CopyAmiToRegion;
  readonly ec2_createAmi: Ec2CreateAmi;
  readonly ec2_createElasticIp: Ec2CreateElasticIp;
  readonly ec2_createKeyPair: Ec2CreateKeyPair;
  readonly ec2_createSecurityGroup: Ec2CreateSecurityGroup;
  readonly ec2_createSnapshot: Ec2CreateSnapshot;
  readonly ec2_createVolume: Ec2CreateVolume;
  readonly ec2_deleteAmi: Ec2DeleteAmi;
  readonly ec2_deleteElasticIp: Ec2DeleteElasticIp;
  readonly ec2_deleteKeyPair: Ec2DeleteKeyPair;
  readonly ec2_deleteSecurityGroup: Ec2DeleteSecurityGroup;
  readonly ec2_deleteSnapshot: Ec2DeleteSnapshot;
  readonly ec2_deleteVolume: Ec2DeleteVolume;
  readonly ec2_editAmiPermission: Ec2EditAmiPermission;
  readonly ec2_editInstanceElasticIp: Ec2EditInstanceElasticIp;
  readonly ec2_editInstanceShutdownBehavior: Ec2EditInstanceShutdownBehavior;
  readonly ec2_editInstanceTerminationProtection: Ec2EditInstanceTerminationProtection;
  readonly ec2_editInstanceType: Ec2EditInstanceType;
  readonly ec2_editInstanceUserData: Ec2EditInstanceUserData;
  readonly ec2_editSecurityGroupPermission: Ec2EditSecurityGroupPermission;
  readonly ec2_editVolumeAttachment: Ec2EditVolumeAttachment;
  readonly ec2_exportPrivateKey: Ec2ExportPrivateKey;
  readonly ec2_importPrivateKey: Ec2ImportPrivateKey;
  readonly ec2_launchInstance: Ec2LaunchInstance;
  readonly ec2_openInstances: Ec2OpenInstances;
  readonly ec2_openAMIs: Ec2OpenAMIs;
  readonly ec2_openElasticIPs: Ec2OpenElasticIPs;
  readonly ec2_openKeyPairs: Ec2OpenKeyPairs;
  readonly ec2_openSecurityGroups: Ec2OpenSecurityGroups;
  readonly ec2_openVolumes: Ec2OpenVolumes;
  readonly ec2_viewInstanceSystemLog: Ec2ViewInstanceSystemLog;
  readonly ecs_openCluster: EcsOpenCluster;
  readonly ec2_viewInstanceUserData: Ec2ViewInstanceUserData;
  readonly ecs_enableExecuteCommand: EcsEnableExecuteCommand;
  readonly ecs_disableExecuteCommand: EcsDisableExecuteCommand;
  readonly ecs_runExecuteCommand: EcsRunExecuteCommand;
  readonly ecr_copyRepositoryUri: EcrCopyRepositoryUri;
  readonly ecr_copyTagUri: EcrCopyTagUri;
  readonly ecr_createRepository: EcrCreateRepository;
  readonly ecr_deleteRepository: EcrDeleteRepository;
  readonly ecr_deleteTags: EcrDeleteTags;
  readonly ecr_deployImage: EcrDeployImage;
  readonly ecs_deployScheduledTask: EcsDeployScheduledTask;
  readonly ecs_deployService: EcsDeployService;
  readonly ecs_deployTask: EcsDeployTask;
  readonly ecs_publishWizard: EcsPublishWizard;
  readonly ecs_openRepository: EcsOpenRepository;
  readonly ecs_deleteService: EcsDeleteService;
  readonly ecs_editService: EcsEditService;
  readonly ecs_deleteCluster: EcsDeleteCluster;
  readonly ecs_stopTask: EcsStopTask;
  readonly ecs_deleteScheduledTask: EcsDeleteScheduledTask;
  readonly feedback_result: FeedbackResult;
  readonly file_editAwsFile: FileEditAwsFile;
  readonly iam_openRole: IamOpenRole;
  readonly iam_openGroup: IamOpenGroup;
  readonly iam_openUser: IamOpenUser;
  readonly iam_open: IamOpen;
  readonly iam_create: IamCreate;
  readonly iam_delete: IamDelete;
  readonly iam_edit: IamEdit;
  readonly iam_createUserAccessKey: IamCreateUserAccessKey;
  readonly iam_deleteUserAccessKey: IamDeleteUserAccessKey;
  readonly lambda_delete: LambdaDelete;
  readonly lambda_configure: LambdaConfigure;
  readonly lambda_create: LambdaCreate;
  readonly lambda_createProject: LambdaCreateProject;
  readonly lambda_goToHandler: LambdaGoToHandler;
  readonly lambda_editFunction: LambdaEditFunction;
  readonly lambda_invokeRemote: LambdaInvokeRemote;
  readonly lambda_invokeLocal: LambdaInvokeLocal;
  readonly lambda_import: LambdaImport;
  readonly lambda_updateFunctionCode: LambdaUpdateFunctionCode;
  readonly lambda_deploy: LambdaDeploy;
  readonly lambda_publishWizard: LambdaPublishWizard;
  readonly cloudformation_delete: CloudformationDelete;
  readonly rds_getCredentials: RdsGetCredentials;
  readonly rds_openInstances: RdsOpenInstances;
  readonly rds_openSecurityGroups: RdsOpenSecurityGroups;
  readonly rds_openSubnets: RdsOpenSubnets;
  readonly rds_launchInstance: RdsLaunchInstance;
  readonly rds_createSecurityGroup: RdsCreateSecurityGroup;
  readonly rds_createSubnetGroup: RdsCreateSubnetGroup;
  readonly rds_deleteInstance: RdsDeleteInstance;
  readonly rds_deleteSecurityGroup: RdsDeleteSecurityGroup;
  readonly rds_deleteSubnetGroup: RdsDeleteSubnetGroup;
  readonly rds_createConnectionConfiguration: RdsCreateConnectionConfiguration;
  readonly redshift_getCredentials: RedshiftGetCredentials;
  readonly redshift_createConnectionConfiguration: RedshiftCreateConnectionConfiguration;
  readonly sam_deploy: SamDeploy;
  readonly sam_sync: SamSync;
  readonly sam_init: SamInit;
  readonly schemas_view: SchemasView;
  readonly schemas_download: SchemasDownload;
  readonly schemas_search: SchemasSearch;
  readonly session_start: SessionStart;
  readonly session_end: SessionEnd;
  readonly s3_copyBucketName: S3CopyBucketName;
  readonly s3_copyPath: S3CopyPath;
  readonly s3_copyUri: S3CopyUri;
  readonly s3_copyUrl: S3CopyUrl;
  readonly s3_createBucket: S3CreateBucket;
  readonly s3_deleteBucket: S3DeleteBucket;
  readonly s3_deleteObject: S3DeleteObject;
  readonly s3_createFolder: S3CreateFolder;
  readonly s3_downloadObject: S3DownloadObject;
  readonly s3_downloadObjects: S3DownloadObjects;
  readonly s3_uploadObject: S3UploadObject;
  readonly s3_renameObject: S3RenameObject;
  readonly s3_uploadObjects: S3UploadObjects;
  readonly s3_openEditor: S3OpenEditor;
  readonly s3_editObject: S3EditObject;
  readonly s3_openBucketProperties: S3OpenBucketProperties;
  readonly s3_openMultipartUpload: S3OpenMultipartUpload;
  readonly toolkit_init: ToolkitInit;
  readonly toolkit_viewLogs: ToolkitViewLogs;
  readonly sqs_openQueue: SqsOpenQueue;
  readonly sqs_createQueue: SqsCreateQueue;
  readonly sqs_sendMessage: SqsSendMessage;
  readonly sqs_deleteMessages: SqsDeleteMessages;
  readonly sqs_subscribeSns: SqsSubscribeSns;
  readonly sqs_configureLambdaTrigger: SqsConfigureLambdaTrigger;
  readonly sqs_editQueueParameters: SqsEditQueueParameters;
  readonly sqs_purgeQueue: SqsPurgeQueue;
  readonly sqs_deleteQueue: SqsDeleteQueue;
  readonly sns_createTopic: SnsCreateTopic;
  readonly sns_createSubscription: SnsCreateSubscription;
  readonly sns_openTopic: SnsOpenTopic;
  readonly sns_openSubscriptions: SnsOpenSubscriptions;
  readonly sns_deleteTopic: SnsDeleteTopic;
  readonly sns_deleteSubscription: SnsDeleteSubscription;
  readonly sns_publishMessage: SnsPublishMessage;
  readonly vpc_openRouteTables: VpcOpenRouteTables;
  readonly vpc_openGateways: VpcOpenGateways;
  readonly vpc_openACLs: VpcOpenACLs;
  readonly vpc_openSubnets: VpcOpenSubnets;
  readonly vpc_openVPCs: VpcOpenVPCs;
  readonly cloudwatchinsights_openEditor: CloudwatchinsightsOpenEditor;
  readonly cloudwatchinsights_executeQuery: CloudwatchinsightsExecuteQuery;
  readonly cloudwatchinsights_saveQuery: CloudwatchinsightsSaveQuery;
  readonly cloudwatchinsights_retrieveQuery: CloudwatchinsightsRetrieveQuery;
  readonly cloudwatchinsights_openDetailedLogRecord: CloudwatchinsightsOpenDetailedLogRecord;
  readonly toolkit_getExternalResource: ToolkitGetExternalResource;
  readonly dynamicresource_getResource: DynamicresourceGetResource;
  readonly dynamicresource_listResource: DynamicresourceListResource;
  readonly dynamicresource_selectResources: DynamicresourceSelectResources;
  readonly dynamicresource_copyIdentifier: DynamicresourceCopyIdentifier;
  readonly dynamicresource_mutateResource: DynamicresourceMutateResource;
  readonly aws_experimentActivation: AwsExperimentActivation;
  readonly aws_toolInstallation: AwsToolInstallation;
  readonly aws_modifySetting: AwsModifySetting;
  readonly ui_click: UiClick;
  readonly deeplink_open: DeeplinkOpen;
  readonly codewhisperer_codePercentage: CodewhispererCodePercentage;
  readonly codewhisperer_securityScan: CodewhispererSecurityScan;
  readonly codewhisperer_serviceInvocation: CodewhispererServiceInvocation;
  readonly codewhisperer_blockedInvocation: CodewhispererBlockedInvocation;
  readonly codewhisperer_userDecision: CodewhispererUserDecision;
  readonly codewhisperer_userTriggerDecision: CodewhispererUserTriggerDecision;
  readonly codewhisperer_userModification: CodewhispererUserModification;
  readonly codewhisperer_perceivedLatency: CodewhispererPerceivedLatency;
  readonly codewhisperer_clientComponentLatency: CodewhispererClientComponentLatency;
  readonly codecatalyst_createDevEnvironment: CodecatalystCreateDevEnvironment;
  readonly codecatalyst_updateDevEnvironmentSettings: CodecatalystUpdateDevEnvironmentSettings;
  readonly codecatalyst_updateDevfile: CodecatalystUpdateDevfile;
  readonly codecatalyst_localClone: CodecatalystLocalClone;
  readonly codecatalyst_connect: CodecatalystConnect;
  readonly codecatalyst_devEnvironmentWorkflowStatistic: CodecatalystDevEnvironmentWorkflowStatistic;
  readonly vscode_executeCommand: VscodeExecuteCommand;
  readonly ssm_createDocument: SsmCreateDocument;
  readonly ssm_deleteDocument: SsmDeleteDocument;
  readonly ssm_executeDocument: SsmExecuteDocument;
  readonly ssm_openDocument: SsmOpenDocument;
  readonly ssm_publishDocument: SsmPublishDocument;
  readonly ssm_updateDocumentVersion: SsmUpdateDocumentVersion;
  readonly stepfunctions_createStateMachineFromTemplate: StepfunctionsCreateStateMachineFromTemplate;
  readonly stepfunctions_downloadStateMachineDefinition: StepfunctionsDownloadStateMachineDefinition;
  readonly stepfunctions_executeStateMachine: StepfunctionsExecuteStateMachine;
  readonly stepfunctions_executeStateMachineView: StepfunctionsExecuteStateMachineView;
  readonly stepfunctions_previewstatemachine: StepfunctionsPreviewstatemachine;
  readonly vscode_activeRegions: VscodeActiveRegions;
  readonly vscode_viewLogs: VscodeViewLogs;
  readonly aws_showExplorerErrorDetails: AwsShowExplorerErrorDetails;
  readonly aws_showRegion: AwsShowRegion;
  readonly aws_hideRegion: AwsHideRegion;
  readonly sam_detect: SamDetect;
  readonly cdk_explorerDisabled: CdkExplorerDisabled;
  readonly cdk_explorerEnabled: CdkExplorerEnabled;
  readonly cdk_appExpanded: CdkAppExpanded;
  readonly cdk_provideFeedback: CdkProvideFeedback;
  readonly cdk_help: CdkHelp;
  readonly cdk_refreshExplorer: CdkRefreshExplorer;
  readonly sam_attachDebugger: SamAttachDebugger;
  readonly sam_openConfigUi: SamOpenConfigUi;
}

export type MetricName = keyof MetricShapes;

export const definitions: Record<string, MetricDefinition> = {
  apigateway_copyUrl: { unit: "None", passive: false, requiredMetadata: [] },
  apigateway_invokeLocal: {
    unit: "None",
    passive: false,
    requiredMetadata: ["debug"],
  },
  apigateway_invokeRemote: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  apigateway_startLocalServer: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  apprunner_openServiceUrl: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  apprunner_copyServiceUrl: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  apprunner_createService: {
    unit: "None",
    passive: false,
    requiredMetadata: ["appRunnerServiceSource"],
  },
  apprunner_pauseService: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  apprunner_resumeService: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  apprunner_deleteService: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  apprunner_startDeployment: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  apprunner_viewApplicationLogs: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  apprunner_viewServiceLogs: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  aws_copyArn: {
    unit: "None",
    passive: false,
    requiredMetadata: ["serviceType"],
  },
  aws_deleteResource: {
    unit: "None",
    passive: false,
    requiredMetadata: ["serviceType"],
  },
  aws_setCredentials: { unit: "None", passive: false, requiredMetadata: [] },
  aws_setRegion: { unit: "None", passive: false, requiredMetadata: [] },
  aws_setPartition: {
    unit: "None",
    passive: false,
    requiredMetadata: ["partitionId"],
  },
  aws_openCredentials: { unit: "None", passive: false, requiredMetadata: [] },
  aws_openUrl: { unit: "None", passive: false, requiredMetadata: [] },
  aws_saveCredentials: { unit: "None", passive: false, requiredMetadata: [] },
  aws_modifyCredentials: {
    unit: "None",
    passive: false,
    requiredMetadata: ["credentialModification", "source"],
  },
  aws_loadCredentials: {
    unit: "Count",
    passive: true,
    requiredMetadata: ["credentialSourceId"],
  },
  aws_createCredentials: { unit: "None", passive: false, requiredMetadata: [] },
  aws_injectCredentials: { unit: "None", passive: false, requiredMetadata: [] },
  aws_validateCredentials: {
    unit: "None",
    passive: true,
    requiredMetadata: [],
  },
  aws_refreshCredentials: { unit: "None", passive: true, requiredMetadata: [] },
  aws_loginWithBrowser: { unit: "None", passive: false, requiredMetadata: [] },
  aws_help: { unit: "None", passive: false, requiredMetadata: [] },
  aws_helpQuickstart: { unit: "None", passive: true, requiredMetadata: [] },
  aws_showExtensionSource: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  aws_refreshExplorer: { unit: "None", passive: false, requiredMetadata: [] },
  aws_expandExplorerNode: {
    unit: "None",
    passive: false,
    requiredMetadata: ["serviceType"],
  },
  aws_reportPluginIssue: { unit: "None", passive: false, requiredMetadata: [] },
  beanstalk_deploy: {
    unit: "None",
    passive: false,
    requiredMetadata: ["initialDeploy"],
  },
  beanstalk_publishWizard: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  beanstalk_openApplication: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  beanstalk_openEnvironment: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  beanstalk_deleteApplication: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  beanstalk_deleteEnvironment: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  beanstalk_restartApplication: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  beanstalk_rebuildEnvironment: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  beanstalk_editEnvironment: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudfront_openDistribution: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudfront_openStreamingDistribution: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudfront_openInvalidationRequest: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudfront_deleteDistribution: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudfront_deleteStreamingDistribution: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudfront_createDistribution: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudfront_createStreamingDistribution: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_copyArn: {
    unit: "None",
    passive: false,
    requiredMetadata: ["cloudWatchResourceType"],
  },
  cloudwatchlogs_open: {
    unit: "None",
    passive: false,
    requiredMetadata: ["cloudWatchResourceType", "source"],
  },
  cloudwatchlogs_openGroup: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_openStream: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_delete: {
    unit: "None",
    passive: false,
    requiredMetadata: ["cloudWatchResourceType"],
  },
  cloudwatchlogs_download: {
    unit: "Bytes",
    passive: false,
    requiredMetadata: ["cloudWatchResourceType"],
  },
  cloudwatchlogs_downloadStreamToFile: {
    unit: "Bytes",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_openStreamInEditor: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_viewCurrentMessagesInEditor: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_wrapEvents: {
    unit: "None",
    passive: false,
    requiredMetadata: ["enabled"],
  },
  cloudwatchlogs_tailStream: {
    unit: "None",
    passive: false,
    requiredMetadata: ["enabled"],
  },
  cloudwatchlogs_refresh: {
    unit: "None",
    passive: false,
    requiredMetadata: ["cloudWatchResourceType"],
  },
  cloudwatchlogs_refreshGroup: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_refreshStream: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_filter: {
    unit: "None",
    passive: false,
    requiredMetadata: ["cloudWatchResourceType"],
  },
  cloudwatchlogs_searchStream: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_searchGroup: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchlogs_showEventsAround: {
    unit: "Milliseconds",
    passive: false,
    requiredMetadata: [],
  },
  cloudformation_createProject: {
    unit: "None",
    passive: false,
    requiredMetadata: ["templateName"],
  },
  cloudformation_deploy: {
    unit: "None",
    passive: false,
    requiredMetadata: ["initialDeploy"],
  },
  cloudformation_publishWizard: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudformation_open: { unit: "None", passive: false, requiredMetadata: [] },
  codecommit_cloneRepo: { unit: "None", passive: false, requiredMetadata: [] },
  codecommit_createRepo: { unit: "None", passive: false, requiredMetadata: [] },
  codecommit_setCredentials: {
    unit: "None",
    passive: true,
    requiredMetadata: [],
  },
  dynamodb_createTable: { unit: "None", passive: false, requiredMetadata: [] },
  dynamodb_deleteTable: { unit: "None", passive: false, requiredMetadata: [] },
  dynamodb_edit: {
    unit: "None",
    passive: false,
    requiredMetadata: ["dynamoDbTarget"],
  },
  dynamodb_fetchRecords: {
    unit: "None",
    passive: false,
    requiredMetadata: ["dynamoDbFetchType"],
  },
  dynamodb_openTable: { unit: "None", passive: false, requiredMetadata: [] },
  dynamodb_view: {
    unit: "None",
    passive: false,
    requiredMetadata: ["dynamoDbTarget"],
  },
  ec2_changeState: {
    unit: "None",
    passive: false,
    requiredMetadata: ["ec2InstanceState"],
  },
  ec2_clearPrivateKey: { unit: "Count", passive: false, requiredMetadata: [] },
  ec2_connectToInstance: {
    unit: "None",
    passive: false,
    requiredMetadata: ["ec2ConnectionType"],
  },
  ec2_copyAmiToRegion: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_createAmi: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_createElasticIp: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_createKeyPair: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_createSecurityGroup: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ec2_createSnapshot: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_createVolume: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_deleteAmi: { unit: "Count", passive: false, requiredMetadata: [] },
  ec2_deleteElasticIp: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_deleteKeyPair: { unit: "Count", passive: false, requiredMetadata: [] },
  ec2_deleteSecurityGroup: {
    unit: "Count",
    passive: false,
    requiredMetadata: [],
  },
  ec2_deleteSnapshot: { unit: "Count", passive: false, requiredMetadata: [] },
  ec2_deleteVolume: { unit: "Count", passive: false, requiredMetadata: [] },
  ec2_editAmiPermission: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_editInstanceElasticIp: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ec2_editInstanceShutdownBehavior: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ec2_editInstanceTerminationProtection: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ec2_editInstanceType: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_editInstanceUserData: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ec2_editSecurityGroupPermission: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ec2_editVolumeAttachment: {
    unit: "None",
    passive: false,
    requiredMetadata: ["enabled"],
  },
  ec2_exportPrivateKey: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_importPrivateKey: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_launchInstance: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_openInstances: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_openAMIs: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_openElasticIPs: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_openKeyPairs: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_openSecurityGroups: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ec2_openVolumes: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_viewInstanceSystemLog: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ecs_openCluster: { unit: "None", passive: false, requiredMetadata: [] },
  ec2_viewInstanceUserData: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ecs_enableExecuteCommand: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ecs_disableExecuteCommand: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  ecs_runExecuteCommand: {
    unit: "None",
    passive: false,
    requiredMetadata: ["ecsExecuteCommandType"],
  },
  ecr_copyRepositoryUri: { unit: "None", passive: false, requiredMetadata: [] },
  ecr_copyTagUri: { unit: "None", passive: false, requiredMetadata: [] },
  ecr_createRepository: { unit: "None", passive: false, requiredMetadata: [] },
  ecr_deleteRepository: { unit: "None", passive: false, requiredMetadata: [] },
  ecr_deleteTags: { unit: "Count", passive: false, requiredMetadata: [] },
  ecr_deployImage: { unit: "None", passive: false, requiredMetadata: [] },
  ecs_deployScheduledTask: {
    unit: "None",
    passive: false,
    requiredMetadata: ["ecsLaunchType"],
  },
  ecs_deployService: {
    unit: "None",
    passive: false,
    requiredMetadata: ["ecsLaunchType"],
  },
  ecs_deployTask: {
    unit: "None",
    passive: false,
    requiredMetadata: ["ecsLaunchType"],
  },
  ecs_publishWizard: { unit: "None", passive: false, requiredMetadata: [] },
  ecs_openRepository: { unit: "None", passive: false, requiredMetadata: [] },
  ecs_deleteService: { unit: "None", passive: false, requiredMetadata: [] },
  ecs_editService: { unit: "None", passive: false, requiredMetadata: [] },
  ecs_deleteCluster: { unit: "None", passive: false, requiredMetadata: [] },
  ecs_stopTask: { unit: "Count", passive: false, requiredMetadata: [] },
  ecs_deleteScheduledTask: {
    unit: "Count",
    passive: false,
    requiredMetadata: [],
  },
  feedback_result: { unit: "None", passive: false, requiredMetadata: [] },
  file_editAwsFile: {
    unit: "None",
    passive: false,
    requiredMetadata: ["awsFiletype"],
  },
  iam_openRole: { unit: "None", passive: false, requiredMetadata: [] },
  iam_openGroup: { unit: "None", passive: false, requiredMetadata: [] },
  iam_openUser: { unit: "None", passive: false, requiredMetadata: [] },
  iam_open: {
    unit: "None",
    passive: false,
    requiredMetadata: ["iamResourceType"],
  },
  iam_create: {
    unit: "None",
    passive: false,
    requiredMetadata: ["iamResourceType"],
  },
  iam_delete: {
    unit: "None",
    passive: false,
    requiredMetadata: ["iamResourceType"],
  },
  iam_edit: {
    unit: "None",
    passive: false,
    requiredMetadata: ["iamResourceType"],
  },
  iam_createUserAccessKey: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  iam_deleteUserAccessKey: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  lambda_delete: { unit: "None", passive: false, requiredMetadata: [] },
  lambda_configure: { unit: "None", passive: false, requiredMetadata: [] },
  lambda_create: {
    unit: "None",
    passive: false,
    requiredMetadata: ["runtime"],
  },
  lambda_createProject: {
    unit: "None",
    passive: false,
    requiredMetadata: ["language", "templateName"],
  },
  lambda_goToHandler: { unit: "None", passive: false, requiredMetadata: [] },
  lambda_editFunction: {
    unit: "None",
    passive: false,
    requiredMetadata: ["lambdaPackageType"],
  },
  lambda_invokeRemote: { unit: "None", passive: false, requiredMetadata: [] },
  lambda_invokeLocal: {
    unit: "None",
    passive: false,
    requiredMetadata: ["lambdaPackageType", "debug"],
  },
  lambda_import: { unit: "None", passive: false, requiredMetadata: [] },
  lambda_updateFunctionCode: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  lambda_deploy: {
    unit: "None",
    passive: false,
    requiredMetadata: ["lambdaPackageType", "initialDeploy"],
  },
  lambda_publishWizard: { unit: "None", passive: false, requiredMetadata: [] },
  cloudformation_delete: { unit: "None", passive: false, requiredMetadata: [] },
  rds_getCredentials: {
    unit: "Milliseconds",
    passive: false,
    requiredMetadata: ["databaseCredentials", "databaseEngine"],
  },
  rds_openInstances: { unit: "None", passive: false, requiredMetadata: [] },
  rds_openSecurityGroups: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  rds_openSubnets: { unit: "None", passive: false, requiredMetadata: [] },
  rds_launchInstance: { unit: "None", passive: false, requiredMetadata: [] },
  rds_createSecurityGroup: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  rds_createSubnetGroup: { unit: "None", passive: false, requiredMetadata: [] },
  rds_deleteInstance: { unit: "None", passive: false, requiredMetadata: [] },
  rds_deleteSecurityGroup: {
    unit: "Count",
    passive: false,
    requiredMetadata: [],
  },
  rds_deleteSubnetGroup: {
    unit: "Count",
    passive: false,
    requiredMetadata: [],
  },
  rds_createConnectionConfiguration: {
    unit: "None",
    passive: false,
    requiredMetadata: ["databaseCredentials"],
  },
  redshift_getCredentials: {
    unit: "Milliseconds",
    passive: false,
    requiredMetadata: ["databaseCredentials"],
  },
  redshift_createConnectionConfiguration: {
    unit: "None",
    passive: false,
    requiredMetadata: ["databaseCredentials"],
  },
  sam_deploy: { unit: "None", passive: false, requiredMetadata: [] },
  sam_sync: {
    unit: "None",
    passive: false,
    requiredMetadata: ["syncedResources", "lambdaPackageType"],
  },
  sam_init: { unit: "None", passive: false, requiredMetadata: [] },
  schemas_view: { unit: "None", passive: false, requiredMetadata: [] },
  schemas_download: { unit: "None", passive: false, requiredMetadata: [] },
  schemas_search: { unit: "None", passive: false, requiredMetadata: [] },
  session_start: { unit: "None", passive: true, requiredMetadata: [] },
  session_end: { unit: "None", passive: true, requiredMetadata: [] },
  s3_copyBucketName: { unit: "None", passive: false, requiredMetadata: [] },
  s3_copyPath: { unit: "None", passive: false, requiredMetadata: [] },
  s3_copyUri: { unit: "None", passive: false, requiredMetadata: [] },
  s3_copyUrl: { unit: "None", passive: false, requiredMetadata: ["presigned"] },
  s3_createBucket: { unit: "None", passive: false, requiredMetadata: [] },
  s3_deleteBucket: { unit: "None", passive: false, requiredMetadata: [] },
  s3_deleteObject: { unit: "None", passive: false, requiredMetadata: [] },
  s3_createFolder: { unit: "None", passive: false, requiredMetadata: [] },
  s3_downloadObject: { unit: "None", passive: false, requiredMetadata: [] },
  s3_downloadObjects: { unit: "Count", passive: false, requiredMetadata: [] },
  s3_uploadObject: { unit: "None", passive: false, requiredMetadata: [] },
  s3_renameObject: { unit: "None", passive: false, requiredMetadata: [] },
  s3_uploadObjects: { unit: "Count", passive: false, requiredMetadata: [] },
  s3_openEditor: { unit: "None", passive: false, requiredMetadata: [] },
  s3_editObject: { unit: "Count", passive: false, requiredMetadata: [] },
  s3_openBucketProperties: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  s3_openMultipartUpload: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  toolkit_init: { unit: "None", passive: true, requiredMetadata: [] },
  toolkit_viewLogs: { unit: "None", passive: false, requiredMetadata: [] },
  sqs_openQueue: {
    unit: "None",
    passive: false,
    requiredMetadata: ["sqsQueueType"],
  },
  sqs_createQueue: { unit: "None", passive: false, requiredMetadata: [] },
  sqs_sendMessage: {
    unit: "None",
    passive: false,
    requiredMetadata: ["sqsQueueType"],
  },
  sqs_deleteMessages: {
    unit: "Count",
    passive: false,
    requiredMetadata: ["sqsQueueType"],
  },
  sqs_subscribeSns: {
    unit: "None",
    passive: false,
    requiredMetadata: ["sqsQueueType"],
  },
  sqs_configureLambdaTrigger: {
    unit: "None",
    passive: false,
    requiredMetadata: ["sqsQueueType"],
  },
  sqs_editQueueParameters: {
    unit: "None",
    passive: false,
    requiredMetadata: ["sqsQueueType"],
  },
  sqs_purgeQueue: {
    unit: "None",
    passive: false,
    requiredMetadata: ["sqsQueueType"],
  },
  sqs_deleteQueue: { unit: "None", passive: false, requiredMetadata: [] },
  sns_createTopic: { unit: "None", passive: false, requiredMetadata: [] },
  sns_createSubscription: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  sns_openTopic: { unit: "None", passive: false, requiredMetadata: [] },
  sns_openSubscriptions: { unit: "None", passive: false, requiredMetadata: [] },
  sns_deleteTopic: { unit: "None", passive: false, requiredMetadata: [] },
  sns_deleteSubscription: {
    unit: "Count",
    passive: false,
    requiredMetadata: [],
  },
  sns_publishMessage: { unit: "None", passive: false, requiredMetadata: [] },
  vpc_openRouteTables: { unit: "None", passive: false, requiredMetadata: [] },
  vpc_openGateways: { unit: "None", passive: false, requiredMetadata: [] },
  vpc_openACLs: { unit: "None", passive: false, requiredMetadata: [] },
  vpc_openSubnets: { unit: "None", passive: false, requiredMetadata: [] },
  vpc_openVPCs: { unit: "None", passive: false, requiredMetadata: [] },
  cloudwatchinsights_openEditor: {
    unit: "None",
    passive: false,
    requiredMetadata: ["insightsDialogOpenSource"],
  },
  cloudwatchinsights_executeQuery: {
    unit: "None",
    passive: false,
    requiredMetadata: ["insightsQueryTimeType", "insightsQueryStringType"],
  },
  cloudwatchinsights_saveQuery: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchinsights_retrieveQuery: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  cloudwatchinsights_openDetailedLogRecord: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  toolkit_getExternalResource: {
    unit: "None",
    passive: true,
    requiredMetadata: ["url"],
  },
  dynamicresource_getResource: {
    unit: "None",
    passive: false,
    requiredMetadata: ["resourceType"],
  },
  dynamicresource_listResource: {
    unit: "None",
    passive: false,
    requiredMetadata: ["resourceType"],
  },
  dynamicresource_selectResources: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  dynamicresource_copyIdentifier: {
    unit: "None",
    passive: false,
    requiredMetadata: ["resourceType"],
  },
  dynamicresource_mutateResource: {
    unit: "None",
    passive: false,
    requiredMetadata: ["resourceType", "dynamicResourceOperation"],
  },
  aws_experimentActivation: {
    unit: "None",
    passive: false,
    requiredMetadata: ["experimentId", "experimentState"],
  },
  aws_toolInstallation: {
    unit: "None",
    passive: true,
    requiredMetadata: ["toolId"],
  },
  aws_modifySetting: {
    unit: "None",
    passive: false,
    requiredMetadata: ["settingId"],
  },
  ui_click: { unit: "None", passive: false, requiredMetadata: ["elementId"] },
  deeplink_open: { unit: "None", passive: true, requiredMetadata: ["source"] },
  codewhisperer_codePercentage: {
    unit: "None",
    passive: true,
    requiredMetadata: [
      "codewhispererAcceptedTokens",
      "codewhispererLanguage",
      "codewhispererPercentage",
      "codewhispererTotalTokens",
      "successCount",
    ],
  },
  codewhisperer_securityScan: {
    unit: "None",
    passive: false,
    requiredMetadata: [
      "codewhispererCodeScanLines",
      "codewhispererCodeScanSrcPayloadBytes",
      "codewhispererCodeScanSrcZipFileBytes",
      "codewhispererCodeScanTotalIssues",
      "codewhispererLanguage",
      "contextTruncationDuration",
      "artifactsUploadDuration",
      "codeScanServiceInvocationsDuration",
    ],
  },
  codewhisperer_serviceInvocation: {
    unit: "None",
    passive: false,
    requiredMetadata: [
      "codewhispererCursorOffset",
      "codewhispererLanguage",
      "codewhispererLineNumber",
      "codewhispererTriggerType",
    ],
  },
  codewhisperer_blockedInvocation: {
    unit: "None",
    passive: false,
    requiredMetadata: [
      "codewhispererCursorOffset",
      "codewhispererLanguage",
      "codewhispererLineNumber",
      "codewhispererTriggerType",
    ],
  },
  codewhisperer_userDecision: {
    unit: "None",
    passive: false,
    requiredMetadata: [
      "codewhispererCompletionType",
      "codewhispererLanguage",
      "codewhispererRequestId",
      "codewhispererSuggestionIndex",
      "codewhispererSuggestionReferenceCount",
      "codewhispererSuggestionState",
      "codewhispererTriggerType",
    ],
  },
  codewhisperer_userTriggerDecision: {
    unit: "None",
    passive: false,
    requiredMetadata: [
      "codewhispererFirstRequestId",
      "codewhispererCompletionType",
      "codewhispererLanguage",
      "codewhispererTriggerType",
      "codewhispererLineNumber",
      "codewhispererCursorOffset",
      "codewhispererSuggestionCount",
      "codewhispererSuggestionImportCount",
      "codewhispererTypeaheadLength",
      "codewhispererSuggestionState",
    ],
  },
  codewhisperer_userModification: {
    unit: "None",
    passive: false,
    requiredMetadata: [
      "codewhispererCompletionType",
      "codewhispererLanguage",
      "codewhispererModificationPercentage",
      "codewhispererRequestId",
      "codewhispererSuggestionIndex",
      "codewhispererTriggerType",
    ],
  },
  codewhisperer_perceivedLatency: {
    unit: "None",
    passive: false,
    requiredMetadata: [
      "codewhispererRequestId",
      "codewhispererTriggerType",
      "codewhispererCompletionType",
      "codewhispererLanguage",
    ],
  },
  codewhisperer_clientComponentLatency: {
    unit: "None",
    passive: true,
    requiredMetadata: [
      "codewhispererRequestId",
      "codewhispererSessionId",
      "codewhispererPreprocessingLatency",
      "codewhispererCredentialFetchingLatency",
      "codewhispererPostprocessingLatency",
      "codewhispererFirstCompletionLatency",
      "codewhispererEndToEndLatency",
      "codewhispererAllCompletionsLatency",
      "codewhispererCompletionType",
      "codewhispererTriggerType",
      "codewhispererLanguage",
    ],
  },
  codecatalyst_createDevEnvironment: {
    unit: "None",
    passive: false,
    requiredMetadata: ["userId"],
  },
  codecatalyst_updateDevEnvironmentSettings: {
    unit: "None",
    passive: false,
    requiredMetadata: [
      "userId",
      "codecatalyst_updateDevEnvironmentLocationType",
    ],
  },
  codecatalyst_updateDevfile: {
    unit: "None",
    passive: false,
    requiredMetadata: ["userId"],
  },
  codecatalyst_localClone: {
    unit: "None",
    passive: false,
    requiredMetadata: ["userId"],
  },
  codecatalyst_connect: {
    unit: "None",
    passive: false,
    requiredMetadata: ["userId"],
  },
  codecatalyst_devEnvironmentWorkflowStatistic: {
    unit: "None",
    passive: true,
    requiredMetadata: ["userId", "codecatalyst_devEnvironmentWorkflowStep"],
  },
  vscode_executeCommand: {
    unit: "None",
    passive: true,
    requiredMetadata: ["command", "debounceCount"],
  },
  ssm_createDocument: { unit: "None", passive: false, requiredMetadata: [] },
  ssm_deleteDocument: { unit: "None", passive: false, requiredMetadata: [] },
  ssm_executeDocument: { unit: "None", passive: false, requiredMetadata: [] },
  ssm_openDocument: { unit: "None", passive: false, requiredMetadata: [] },
  ssm_publishDocument: {
    unit: "None",
    passive: false,
    requiredMetadata: ["ssmOperation"],
  },
  ssm_updateDocumentVersion: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  stepfunctions_createStateMachineFromTemplate: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  stepfunctions_downloadStateMachineDefinition: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  stepfunctions_executeStateMachine: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  stepfunctions_executeStateMachineView: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  stepfunctions_previewstatemachine: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  vscode_activeRegions: { unit: "Count", passive: true, requiredMetadata: [] },
  vscode_viewLogs: { unit: "None", passive: false, requiredMetadata: [] },
  aws_showExplorerErrorDetails: {
    unit: "None",
    passive: false,
    requiredMetadata: [],
  },
  aws_showRegion: { unit: "None", passive: false, requiredMetadata: [] },
  aws_hideRegion: { unit: "None", passive: false, requiredMetadata: [] },
  sam_detect: { unit: "None", passive: true, requiredMetadata: [] },
  cdk_explorerDisabled: { unit: "None", passive: false, requiredMetadata: [] },
  cdk_explorerEnabled: { unit: "None", passive: false, requiredMetadata: [] },
  cdk_appExpanded: { unit: "None", passive: false, requiredMetadata: [] },
  cdk_provideFeedback: { unit: "None", passive: false, requiredMetadata: [] },
  cdk_help: { unit: "None", passive: false, requiredMetadata: [] },
  cdk_refreshExplorer: { unit: "None", passive: false, requiredMetadata: [] },
  sam_attachDebugger: {
    unit: "None",
    passive: false,
    requiredMetadata: ["lambdaPackageType", "runtime", "attempts"],
  },
  sam_openConfigUi: { unit: "None", passive: false, requiredMetadata: [] },
};

export type Metadata<T extends MetricBase> = Partial<Omit<T, keyof MetricBase>>;

export interface Metric<T extends MetricBase = MetricBase> {
  readonly name: string;
  /** Adds data to the metric which is preserved for the remainder of the execution context */
  record(data: Metadata<T>): void;
  /** Sends the metric to the telemetry service */
  emit(data?: T): void;
  /** Executes a callback, automatically sending the metric after completion */
  run<U>(fn: (span: this) => U): U;
}

export abstract class TelemetryBase {
  /** Copying an API Gateway remote URL */
  public get apigateway_copyUrl(): Metric<ApigatewayCopyUrl> {
    return this.getMetric("apigateway_copyUrl");
  }

  /** Invoking one simulated API Gateway call using the SAM cli */
  public get apigateway_invokeLocal(): Metric<ApigatewayInvokeLocal> {
    return this.getMetric("apigateway_invokeLocal");
  }

  /** Calling a remote API Gateway */
  public get apigateway_invokeRemote(): Metric<ApigatewayInvokeRemote> {
    return this.getMetric("apigateway_invokeRemote");
  }

  /** Called when starting a local API Gateway server simulator with SAM. Only called when starting it for long running testing, not for single invokes */
  public get apigateway_startLocalServer(): Metric<ApigatewayStartLocalServer> {
    return this.getMetric("apigateway_startLocalServer");
  }

  /** Open the service URL in a browser */
  public get apprunner_openServiceUrl(): Metric<ApprunnerOpenServiceUrl> {
    return this.getMetric("apprunner_openServiceUrl");
  }

  /** Copy the service URL */
  public get apprunner_copyServiceUrl(): Metric<ApprunnerCopyServiceUrl> {
    return this.getMetric("apprunner_copyServiceUrl");
  }

  /** Create an App Runner service */
  public get apprunner_createService(): Metric<ApprunnerCreateService> {
    return this.getMetric("apprunner_createService");
  }

  /** Pause a running App Runner service */
  public get apprunner_pauseService(): Metric<ApprunnerPauseService> {
    return this.getMetric("apprunner_pauseService");
  }

  /** Resume a paused App Runner service */
  public get apprunner_resumeService(): Metric<ApprunnerResumeService> {
    return this.getMetric("apprunner_resumeService");
  }

  /** Delete an App Runner service */
  public get apprunner_deleteService(): Metric<ApprunnerDeleteService> {
    return this.getMetric("apprunner_deleteService");
  }

  /** Start a new deployment for an App Runner service */
  public get apprunner_startDeployment(): Metric<ApprunnerStartDeployment> {
    return this.getMetric("apprunner_startDeployment");
  }

  /** View the App Runner application logs (the logs for your running service) */
  public get apprunner_viewApplicationLogs(): Metric<ApprunnerViewApplicationLogs> {
    return this.getMetric("apprunner_viewApplicationLogs");
  }

  /** View the App Runner service logs (the logs produced by App Runner) */
  public get apprunner_viewServiceLogs(): Metric<ApprunnerViewServiceLogs> {
    return this.getMetric("apprunner_viewServiceLogs");
  }

  /** Copy the ARN of an AWS resource */
  public get aws_copyArn(): Metric<AwsCopyArn> {
    return this.getMetric("aws_copyArn");
  }

  /** Delete an AWS resource */
  public get aws_deleteResource(): Metric<AwsDeleteResource> {
    return this.getMetric("aws_deleteResource");
  }

  /** Select a credentials profile */
  public get aws_setCredentials(): Metric<AwsSetCredentials> {
    return this.getMetric("aws_setCredentials");
  }

  /** A region change occurred */
  public get aws_setRegion(): Metric<AwsSetRegion> {
    return this.getMetric("aws_setRegion");
  }

  /** A partition change occurred */
  public get aws_setPartition(): Metric<AwsSetPartition> {
    return this.getMetric("aws_setPartition");
  }

  /** Open the credentials file */
  public get aws_openCredentials(): Metric<AwsOpenCredentials> {
    return this.getMetric("aws_openCredentials");
  }

  /** Opens a url */
  public get aws_openUrl(): Metric<AwsOpenUrl> {
    return this.getMetric("aws_openUrl");
  }

  /** Save credentials */
  public get aws_saveCredentials(): Metric<AwsSaveCredentials> {
    return this.getMetric("aws_saveCredentials");
  }

  /** Modify credentials (e.g. Add, Edit, Delete) */
  public get aws_modifyCredentials(): Metric<AwsModifyCredentials> {
    return this.getMetric("aws_modifyCredentials");
  }

  /** Load credentials from a credential source */
  public get aws_loadCredentials(): Metric<AwsLoadCredentials> {
    return this.getMetric("aws_loadCredentials");
  }

  /** Create a new credentials file */
  public get aws_createCredentials(): Metric<AwsCreateCredentials> {
    return this.getMetric("aws_createCredentials");
  }

  /** Inject selected AWS credentials into a third-party run (e.g. RunConfiguration) */
  public get aws_injectCredentials(): Metric<AwsInjectCredentials> {
    return this.getMetric("aws_injectCredentials");
  }

  /** Validate credentials when selecting new credentials */
  public get aws_validateCredentials(): Metric<AwsValidateCredentials> {
    return this.getMetric("aws_validateCredentials");
  }

  /** Emitted when credentials are automatically refreshed by the AWS SDK or Toolkit */
  public get aws_refreshCredentials(): Metric<AwsRefreshCredentials> {
    return this.getMetric("aws_refreshCredentials");
  }

  /** Called when a connection requires login using the browser */
  public get aws_loginWithBrowser(): Metric<AwsLoginWithBrowser> {
    return this.getMetric("aws_loginWithBrowser");
  }

  /** Open docs for the extension */
  public get aws_help(): Metric<AwsHelp> {
    return this.getMetric("aws_help");
  }

  /** Open the quickstart guide */
  public get aws_helpQuickstart(): Metric<AwsHelpQuickstart> {
    return this.getMetric("aws_helpQuickstart");
  }

  /** Open the repo for the extension */
  public get aws_showExtensionSource(): Metric<AwsShowExtensionSource> {
    return this.getMetric("aws_showExtensionSource");
  }

  /** Refresh the AWS explorer window */
  public get aws_refreshExplorer(): Metric<AwsRefreshExplorer> {
    return this.getMetric("aws_refreshExplorer");
  }

  /** Expand a service root node in the AWS explorer window */
  public get aws_expandExplorerNode(): Metric<AwsExpandExplorerNode> {
    return this.getMetric("aws_expandExplorerNode");
  }

  /** Report an issue with the plugin */
  public get aws_reportPluginIssue(): Metric<AwsReportPluginIssue> {
    return this.getMetric("aws_reportPluginIssue");
  }

  /** Called when deploying an application to Elastic Beanstalk */
  public get beanstalk_deploy(): Metric<BeanstalkDeploy> {
    return this.getMetric("beanstalk_deploy");
  }

  /** Called when user completes the Elastic Beanstalk publish wizard */
  public get beanstalk_publishWizard(): Metric<BeanstalkPublishWizard> {
    return this.getMetric("beanstalk_publishWizard");
  }

  /** Open a window to view the status of the Beanstalk Application */
  public get beanstalk_openApplication(): Metric<BeanstalkOpenApplication> {
    return this.getMetric("beanstalk_openApplication");
  }

  /** Open a window to view the status of the Beanstalk Environment */
  public get beanstalk_openEnvironment(): Metric<BeanstalkOpenEnvironment> {
    return this.getMetric("beanstalk_openEnvironment");
  }

  /** Called when user deletes a Beanstalk application */
  public get beanstalk_deleteApplication(): Metric<BeanstalkDeleteApplication> {
    return this.getMetric("beanstalk_deleteApplication");
  }

  /** Called when user deletes a Beanstalk environment */
  public get beanstalk_deleteEnvironment(): Metric<BeanstalkDeleteEnvironment> {
    return this.getMetric("beanstalk_deleteEnvironment");
  }

  /** Restart application server for a Beanstalk environment */
  public get beanstalk_restartApplication(): Metric<BeanstalkRestartApplication> {
    return this.getMetric("beanstalk_restartApplication");
  }

  /** Rebuild a Beanstalk environment */
  public get beanstalk_rebuildEnvironment(): Metric<BeanstalkRebuildEnvironment> {
    return this.getMetric("beanstalk_rebuildEnvironment");
  }

  /** Edit configuration of a Beanstalk environment */
  public get beanstalk_editEnvironment(): Metric<BeanstalkEditEnvironment> {
    return this.getMetric("beanstalk_editEnvironment");
  }

  /** Open a window to view the status of the CloudFront Distribution */
  public get cloudfront_openDistribution(): Metric<CloudfrontOpenDistribution> {
    return this.getMetric("cloudfront_openDistribution");
  }

  /** Open a window to view the status of the CloudFront Streaming Distribution */
  public get cloudfront_openStreamingDistribution(): Metric<CloudfrontOpenStreamingDistribution> {
    return this.getMetric("cloudfront_openStreamingDistribution");
  }

  /** Open a window to view the Cloudfront Invalidation requests */
  public get cloudfront_openInvalidationRequest(): Metric<CloudfrontOpenInvalidationRequest> {
    return this.getMetric("cloudfront_openInvalidationRequest");
  }

  /** Called when user deletes a CloudFront Distribution */
  public get cloudfront_deleteDistribution(): Metric<CloudfrontDeleteDistribution> {
    return this.getMetric("cloudfront_deleteDistribution");
  }

  /** Called when user deletes a CloudFront Streaming Distribution */
  public get cloudfront_deleteStreamingDistribution(): Metric<CloudfrontDeleteStreamingDistribution> {
    return this.getMetric("cloudfront_deleteStreamingDistribution");
  }

  /** Create a CloudFront Distribution */
  public get cloudfront_createDistribution(): Metric<CloudfrontCreateDistribution> {
    return this.getMetric("cloudfront_createDistribution");
  }

  /** Create a CloudFront Streaming Distribution */
  public get cloudfront_createStreamingDistribution(): Metric<CloudfrontCreateStreamingDistribution> {
    return this.getMetric("cloudfront_createStreamingDistribution");
  }

  /** Copy the ARN of a CloudWatch Logs entity */
  public get cloudwatchlogs_copyArn(): Metric<CloudwatchlogsCopyArn> {
    return this.getMetric("cloudwatchlogs_copyArn");
  }

  /** Open a CloudWatch Logs entity. ServiceType and source indicate where the request came from (example: while viewing an ECS container) */
  public get cloudwatchlogs_open(): Metric<CloudwatchlogsOpen> {
    return this.getMetric("cloudwatchlogs_open");
  }

  /** Open the CloudWatch Logs group window. ServiceType indicates that it was opened from a different service (like directly from an ECS container) (Deprecated - use cloudwatchlogs_open) */
  public get cloudwatchlogs_openGroup(): Metric<CloudwatchlogsOpenGroup> {
    return this.getMetric("cloudwatchlogs_openGroup");
  }

  /** Open a CloudWatch Logs stream in the window. ServiceType indicates that it was opened from a different service (like directly from an ECS container) (Deprecated - use cloudwatchlogs_open) */
  public get cloudwatchlogs_openStream(): Metric<CloudwatchlogsOpenStream> {
    return this.getMetric("cloudwatchlogs_openStream");
  }

  /** Delete a CloudWatch Logs entity. */
  public get cloudwatchlogs_delete(): Metric<CloudwatchlogsDelete> {
    return this.getMetric("cloudwatchlogs_delete");
  }

  /** Download a CloudWatch Logs entity. Value indicates the final size of the formatted stream in bytes. */
  public get cloudwatchlogs_download(): Metric<CloudwatchlogsDownload> {
    return this.getMetric("cloudwatchlogs_download");
  }

  /** Download a stream to a file on disk. Value indicates the final size of the formatted stream. (Deprecated - use cloudwatchlogs_download) */
  public get cloudwatchlogs_downloadStreamToFile(): Metric<CloudwatchlogsDownloadStreamToFile> {
    return this.getMetric("cloudwatchlogs_downloadStreamToFile");
  }

  /** Download a stream to memory then open in an editor. */
  public get cloudwatchlogs_openStreamInEditor(): Metric<CloudwatchlogsOpenStreamInEditor> {
    return this.getMetric("cloudwatchlogs_openStreamInEditor");
  }

  /** Copy the currently open (possibly filtered) messages to an editor */
  public get cloudwatchlogs_viewCurrentMessagesInEditor(): Metric<CloudwatchlogsViewCurrentMessagesInEditor> {
    return this.getMetric("cloudwatchlogs_viewCurrentMessagesInEditor");
  }

  /** Word wrap events off/on */
  public get cloudwatchlogs_wrapEvents(): Metric<CloudwatchlogsWrapEvents> {
    return this.getMetric("cloudwatchlogs_wrapEvents");
  }

  /** Tail stream off/on */
  public get cloudwatchlogs_tailStream(): Metric<CloudwatchlogsTailStream> {
    return this.getMetric("cloudwatchlogs_tailStream");
  }

  /** Refresh a CloudWatch Logs entity */
  public get cloudwatchlogs_refresh(): Metric<CloudwatchlogsRefresh> {
    return this.getMetric("cloudwatchlogs_refresh");
  }

  /** Refresh group is pressed (Deprecated, use cloudwatchlogs_refresh) */
  public get cloudwatchlogs_refreshGroup(): Metric<CloudwatchlogsRefreshGroup> {
    return this.getMetric("cloudwatchlogs_refreshGroup");
  }

  /** Refresh stream is pressed (Deprecated, use cloudwatchlogs_refresh) */
  public get cloudwatchlogs_refreshStream(): Metric<CloudwatchlogsRefreshStream> {
    return this.getMetric("cloudwatchlogs_refreshStream");
  }

  /** Filters a CloudWatch Logs entity. */
  public get cloudwatchlogs_filter(): Metric<CloudwatchlogsFilter> {
    return this.getMetric("cloudwatchlogs_filter");
  }

  /** Called when a stream is searched */
  public get cloudwatchlogs_searchStream(): Metric<CloudwatchlogsSearchStream> {
    return this.getMetric("cloudwatchlogs_searchStream");
  }

  /** Called when a group is searched */
  public get cloudwatchlogs_searchGroup(): Metric<CloudwatchlogsSearchGroup> {
    return this.getMetric("cloudwatchlogs_searchGroup");
  }

  /** Show event around a time period in ms specified by Value */
  public get cloudwatchlogs_showEventsAround(): Metric<CloudwatchlogsShowEventsAround> {
    return this.getMetric("cloudwatchlogs_showEventsAround");
  }

  /** Called when creating a CloudFormation project */
  public get cloudformation_createProject(): Metric<CloudformationCreateProject> {
    return this.getMetric("cloudformation_createProject");
  }

  /** Called when deploying a CloudFormation template */
  public get cloudformation_deploy(): Metric<CloudformationDeploy> {
    return this.getMetric("cloudformation_deploy");
  }

  /** Called when user completes the CloudFormation template publish wizard */
  public get cloudformation_publishWizard(): Metric<CloudformationPublishWizard> {
    return this.getMetric("cloudformation_publishWizard");
  }

  /** Open a CloudFormation stack in the stack viewer */
  public get cloudformation_open(): Metric<CloudformationOpen> {
    return this.getMetric("cloudformation_open");
  }

  /** A repo is cloned from CodeCommit */
  public get codecommit_cloneRepo(): Metric<CodecommitCloneRepo> {
    return this.getMetric("codecommit_cloneRepo");
  }

  /** A repo is created in CodeCommit */
  public get codecommit_createRepo(): Metric<CodecommitCreateRepo> {
    return this.getMetric("codecommit_createRepo");
  }

  /** A connection is established to CodeCommit to perform actions on repos */
  public get codecommit_setCredentials(): Metric<CodecommitSetCredentials> {
    return this.getMetric("codecommit_setCredentials");
  }

  /** Create a DynamoDB table */
  public get dynamodb_createTable(): Metric<DynamodbCreateTable> {
    return this.getMetric("dynamodb_createTable");
  }

  /** Delete a DynamoDB table */
  public get dynamodb_deleteTable(): Metric<DynamodbDeleteTable> {
    return this.getMetric("dynamodb_deleteTable");
  }

  /** Modify a DynamoDB entity */
  public get dynamodb_edit(): Metric<DynamodbEdit> {
    return this.getMetric("dynamodb_edit");
  }

  /** Fetch records from a DynamoDB table in the table browser */
  public get dynamodb_fetchRecords(): Metric<DynamodbFetchRecords> {
    return this.getMetric("dynamodb_fetchRecords");
  }

  /** Open a DynamoDB table in the table browser */
  public get dynamodb_openTable(): Metric<DynamodbOpenTable> {
    return this.getMetric("dynamodb_openTable");
  }

  /** View a DynamoDB entity */
  public get dynamodb_view(): Metric<DynamodbView> {
    return this.getMetric("dynamodb_view");
  }

  /** Change the state of an EC2 Instance */
  public get ec2_changeState(): Metric<Ec2ChangeState> {
    return this.getMetric("ec2_changeState");
  }

  /** Remove the private key of an EC2 Key Pair from internal storage */
  public get ec2_clearPrivateKey(): Metric<Ec2ClearPrivateKey> {
    return this.getMetric("ec2_clearPrivateKey");
  }

  /** Perform a connection to an EC2 Instance */
  public get ec2_connectToInstance(): Metric<Ec2ConnectToInstance> {
    return this.getMetric("ec2_connectToInstance");
  }

  /** Copy AMI image to another region */
  public get ec2_copyAmiToRegion(): Metric<Ec2CopyAmiToRegion> {
    return this.getMetric("ec2_copyAmiToRegion");
  }

  /** Create an image from an EC2 Instance */
  public get ec2_createAmi(): Metric<Ec2CreateAmi> {
    return this.getMetric("ec2_createAmi");
  }

  /** Create (allocate) an Elastic IP address */
  public get ec2_createElasticIp(): Metric<Ec2CreateElasticIp> {
    return this.getMetric("ec2_createElasticIp");
  }

  /** Create an EC2 Key Pair */
  public get ec2_createKeyPair(): Metric<Ec2CreateKeyPair> {
    return this.getMetric("ec2_createKeyPair");
  }

  /** Create an EC2 security group */
  public get ec2_createSecurityGroup(): Metric<Ec2CreateSecurityGroup> {
    return this.getMetric("ec2_createSecurityGroup");
  }

  /** Create an EC2 volume snapshot */
  public get ec2_createSnapshot(): Metric<Ec2CreateSnapshot> {
    return this.getMetric("ec2_createSnapshot");
  }

  /** Create an EC2 volume */
  public get ec2_createVolume(): Metric<Ec2CreateVolume> {
    return this.getMetric("ec2_createVolume");
  }

  /** Delete (de-register) an AMI image */
  public get ec2_deleteAmi(): Metric<Ec2DeleteAmi> {
    return this.getMetric("ec2_deleteAmi");
  }

  /** Delete (release) an Elastic IP address */
  public get ec2_deleteElasticIp(): Metric<Ec2DeleteElasticIp> {
    return this.getMetric("ec2_deleteElasticIp");
  }

  /** Delete an EC2 Key Pair */
  public get ec2_deleteKeyPair(): Metric<Ec2DeleteKeyPair> {
    return this.getMetric("ec2_deleteKeyPair");
  }

  /** Delete an EC2 security group */
  public get ec2_deleteSecurityGroup(): Metric<Ec2DeleteSecurityGroup> {
    return this.getMetric("ec2_deleteSecurityGroup");
  }

  /** Delete an EC2 Volume Snapshot */
  public get ec2_deleteSnapshot(): Metric<Ec2DeleteSnapshot> {
    return this.getMetric("ec2_deleteSnapshot");
  }

  /** Delete an EC2 Volume */
  public get ec2_deleteVolume(): Metric<Ec2DeleteVolume> {
    return this.getMetric("ec2_deleteVolume");
  }

  /** Edit AMI image permissions */
  public get ec2_editAmiPermission(): Metric<Ec2EditAmiPermission> {
    return this.getMetric("ec2_editAmiPermission");
  }

  /** Associate or disassociate an Elastic IP with an EC2 Instance */
  public get ec2_editInstanceElasticIp(): Metric<Ec2EditInstanceElasticIp> {
    return this.getMetric("ec2_editInstanceElasticIp");
  }

  /** Adjust the shutdown behavior of an EC2 Instance */
  public get ec2_editInstanceShutdownBehavior(): Metric<Ec2EditInstanceShutdownBehavior> {
    return this.getMetric("ec2_editInstanceShutdownBehavior");
  }

  /** Adjust the termination protection of an EC2 Instance */
  public get ec2_editInstanceTerminationProtection(): Metric<Ec2EditInstanceTerminationProtection> {
    return this.getMetric("ec2_editInstanceTerminationProtection");
  }

  /** Adjust the instance type of an EC2 Instance */
  public get ec2_editInstanceType(): Metric<Ec2EditInstanceType> {
    return this.getMetric("ec2_editInstanceType");
  }

  /** Adjust an EC2 Instance's user data */
  public get ec2_editInstanceUserData(): Metric<Ec2EditInstanceUserData> {
    return this.getMetric("ec2_editInstanceUserData");
  }

  /** Alter an EC2 security group permission */
  public get ec2_editSecurityGroupPermission(): Metric<Ec2EditSecurityGroupPermission> {
    return this.getMetric("ec2_editSecurityGroupPermission");
  }

  /** Attach (enabled = true) or detach a volume */
  public get ec2_editVolumeAttachment(): Metric<Ec2EditVolumeAttachment> {
    return this.getMetric("ec2_editVolumeAttachment");
  }

  /** Save the private key of an EC2 Key Pair out to disk */
  public get ec2_exportPrivateKey(): Metric<Ec2ExportPrivateKey> {
    return this.getMetric("ec2_exportPrivateKey");
  }

  /** Store the private key of an EC2 Key Pair in internal storage */
  public get ec2_importPrivateKey(): Metric<Ec2ImportPrivateKey> {
    return this.getMetric("ec2_importPrivateKey");
  }

  /** Launch an EC2 Instance */
  public get ec2_launchInstance(): Metric<Ec2LaunchInstance> {
    return this.getMetric("ec2_launchInstance");
  }

  /** Open a window to view EC2 Instances */
  public get ec2_openInstances(): Metric<Ec2OpenInstances> {
    return this.getMetric("ec2_openInstances");
  }

  /** Open a window to view EC2 AMIs */
  public get ec2_openAMIs(): Metric<Ec2OpenAMIs> {
    return this.getMetric("ec2_openAMIs");
  }

  /** Open a window to view EC2 Elastic IPs */
  public get ec2_openElasticIPs(): Metric<Ec2OpenElasticIPs> {
    return this.getMetric("ec2_openElasticIPs");
  }

  /** Open to view EC2 Key pairs */
  public get ec2_openKeyPairs(): Metric<Ec2OpenKeyPairs> {
    return this.getMetric("ec2_openKeyPairs");
  }

  /** Open a window to view EC2 Security Groups */
  public get ec2_openSecurityGroups(): Metric<Ec2OpenSecurityGroups> {
    return this.getMetric("ec2_openSecurityGroups");
  }

  /** Open a window to view EC2 Volumes */
  public get ec2_openVolumes(): Metric<Ec2OpenVolumes> {
    return this.getMetric("ec2_openVolumes");
  }

  /** View the system log of an EC2 Instance */
  public get ec2_viewInstanceSystemLog(): Metric<Ec2ViewInstanceSystemLog> {
    return this.getMetric("ec2_viewInstanceSystemLog");
  }

  /** Open to view status of an ECS Cluster */
  public get ecs_openCluster(): Metric<EcsOpenCluster> {
    return this.getMetric("ecs_openCluster");
  }

  /** View an EC2 Instance's user data */
  public get ec2_viewInstanceUserData(): Metric<Ec2ViewInstanceUserData> {
    return this.getMetric("ec2_viewInstanceUserData");
  }

  /** Called when ECS execute command is enabled */
  public get ecs_enableExecuteCommand(): Metric<EcsEnableExecuteCommand> {
    return this.getMetric("ecs_enableExecuteCommand");
  }

  /** Called when ECS execute command is disabled */
  public get ecs_disableExecuteCommand(): Metric<EcsDisableExecuteCommand> {
    return this.getMetric("ecs_disableExecuteCommand");
  }

  /** Called when the ECS execute command is run */
  public get ecs_runExecuteCommand(): Metric<EcsRunExecuteCommand> {
    return this.getMetric("ecs_runExecuteCommand");
  }

  /** Called when the user copies the repository uri from a node */
  public get ecr_copyRepositoryUri(): Metric<EcrCopyRepositoryUri> {
    return this.getMetric("ecr_copyRepositoryUri");
  }

  /** Called when the user copies the repository tag uri from a node. The tag uri is the repository uri + : + the tag name */
  public get ecr_copyTagUri(): Metric<EcrCopyTagUri> {
    return this.getMetric("ecr_copyTagUri");
  }

  /** Called when creating a new ECR repository */
  public get ecr_createRepository(): Metric<EcrCreateRepository> {
    return this.getMetric("ecr_createRepository");
  }

  /** Called when deleting an existing ECR repository */
  public get ecr_deleteRepository(): Metric<EcrDeleteRepository> {
    return this.getMetric("ecr_deleteRepository");
  }

  /** Called when deleting a tag in an ECR repository. The operation is a batch operation by default, value represents the number of tags deleted. */
  public get ecr_deleteTags(): Metric<EcrDeleteTags> {
    return this.getMetric("ecr_deleteTags");
  }

  /** Called when deploying an image to ECR */
  public get ecr_deployImage(): Metric<EcrDeployImage> {
    return this.getMetric("ecr_deployImage");
  }

  /** Called when deploying a scheduled task to an ECS cluster */
  public get ecs_deployScheduledTask(): Metric<EcsDeployScheduledTask> {
    return this.getMetric("ecs_deployScheduledTask");
  }

  /** Called when deploying a service to an ECS cluster */
  public get ecs_deployService(): Metric<EcsDeployService> {
    return this.getMetric("ecs_deployService");
  }

  /** Called when deploying a task to an ECS cluster */
  public get ecs_deployTask(): Metric<EcsDeployTask> {
    return this.getMetric("ecs_deployTask");
  }

  /** Called when user completes the ECS publish wizard */
  public get ecs_publishWizard(): Metric<EcsPublishWizard> {
    return this.getMetric("ecs_publishWizard");
  }

  /** Open to view status of an ECS Repository */
  public get ecs_openRepository(): Metric<EcsOpenRepository> {
    return this.getMetric("ecs_openRepository");
  }

  /** Called when user deletes an ECS service */
  public get ecs_deleteService(): Metric<EcsDeleteService> {
    return this.getMetric("ecs_deleteService");
  }

  /** Edit configuration of an ECS service */
  public get ecs_editService(): Metric<EcsEditService> {
    return this.getMetric("ecs_editService");
  }

  /** Delete an ECS cluster */
  public get ecs_deleteCluster(): Metric<EcsDeleteCluster> {
    return this.getMetric("ecs_deleteCluster");
  }

  /** Stop ECS task(s) */
  public get ecs_stopTask(): Metric<EcsStopTask> {
    return this.getMetric("ecs_stopTask");
  }

  /** Delete ECS Scheduled task(s) */
  public get ecs_deleteScheduledTask(): Metric<EcsDeleteScheduledTask> {
    return this.getMetric("ecs_deleteScheduledTask");
  }

  /** Called while submitting in-IDE feedback */
  public get feedback_result(): Metric<FeedbackResult> {
    return this.getMetric("feedback_result");
  }

  /** Use authoring features such as autocompletion, syntax checking, and highlighting, for AWS filetypes (CFN, SAM, etc.). Emit this _once_ per file-editing session for a given file. Ideally this is emitted only if authoring features are used, rather than merely opening or touching a file. */
  public get file_editAwsFile(): Metric<FileEditAwsFile> {
    return this.getMetric("file_editAwsFile");
  }

  /** Open a window to view/edit IAM Role Policy */
  public get iam_openRole(): Metric<IamOpenRole> {
    return this.getMetric("iam_openRole");
  }

  /** Open a window to view/edit IAM Group Policy */
  public get iam_openGroup(): Metric<IamOpenGroup> {
    return this.getMetric("iam_openGroup");
  }

  /** Open a window to view/edit IAM User Configuration */
  public get iam_openUser(): Metric<IamOpenUser> {
    return this.getMetric("iam_openUser");
  }

  /** Open a window to view/edit an IAM resource */
  public get iam_open(): Metric<IamOpen> {
    return this.getMetric("iam_open");
  }

  /** Create an IAM resource */
  public get iam_create(): Metric<IamCreate> {
    return this.getMetric("iam_create");
  }

  /** Delete an IAM resource */
  public get iam_delete(): Metric<IamDelete> {
    return this.getMetric("iam_delete");
  }

  /** Edits policy/configuration associated with an IAM resource */
  public get iam_edit(): Metric<IamEdit> {
    return this.getMetric("iam_edit");
  }

  /** Create Access Key for an IAM user */
  public get iam_createUserAccessKey(): Metric<IamCreateUserAccessKey> {
    return this.getMetric("iam_createUserAccessKey");
  }

  /** Delete Access Key for an IAM user */
  public get iam_deleteUserAccessKey(): Metric<IamDeleteUserAccessKey> {
    return this.getMetric("iam_deleteUserAccessKey");
  }

  /** called when deleting lambdas remotely */
  public get lambda_delete(): Metric<LambdaDelete> {
    return this.getMetric("lambda_delete");
  }

  /** Called when opening the local configuration of a Lambda to edit */
  public get lambda_configure(): Metric<LambdaConfigure> {
    return this.getMetric("lambda_configure");
  }

  /** Called when creating lambdas remotely */
  public get lambda_create(): Metric<LambdaCreate> {
    return this.getMetric("lambda_create");
  }

  /** Called when creating a lambda project */
  public get lambda_createProject(): Metric<LambdaCreateProject> {
    return this.getMetric("lambda_createProject");
  }

  /** Jump to a lambda handler from elsewhere */
  public get lambda_goToHandler(): Metric<LambdaGoToHandler> {
    return this.getMetric("lambda_goToHandler");
  }

  /** Called when creating lambdas remotely */
  public get lambda_editFunction(): Metric<LambdaEditFunction> {
    return this.getMetric("lambda_editFunction");
  }

  /** Called when invoking lambdas remotely */
  public get lambda_invokeRemote(): Metric<LambdaInvokeRemote> {
    return this.getMetric("lambda_invokeRemote");
  }

  /** Called when invoking lambdas locally (with SAM in most toolkits) */
  public get lambda_invokeLocal(): Metric<LambdaInvokeLocal> {
    return this.getMetric("lambda_invokeLocal");
  }

  /** Called when importing a remote Lambda function */
  public get lambda_import(): Metric<LambdaImport> {
    return this.getMetric("lambda_import");
  }

  /** Called when updating a Lambda function's code outside the context of a SAM template */
  public get lambda_updateFunctionCode(): Metric<LambdaUpdateFunctionCode> {
    return this.getMetric("lambda_updateFunctionCode");
  }

  /** Called when deploying a Lambda Function */
  public get lambda_deploy(): Metric<LambdaDeploy> {
    return this.getMetric("lambda_deploy");
  }

  /** Called when user completes the Lambda publish wizard */
  public get lambda_publishWizard(): Metric<LambdaPublishWizard> {
    return this.getMetric("lambda_publishWizard");
  }

  /** Called when deleting a cloudformation stack */
  public get cloudformation_delete(): Metric<CloudformationDelete> {
    return this.getMetric("cloudformation_delete");
  }

  /** Called when getting IAM/SecretsManager credentials for a RDS database. Value represents how long it takes in ms. */
  public get rds_getCredentials(): Metric<RdsGetCredentials> {
    return this.getMetric("rds_getCredentials");
  }

  /** Open a window to view RDS DB Instances */
  public get rds_openInstances(): Metric<RdsOpenInstances> {
    return this.getMetric("rds_openInstances");
  }

  /** Open a window to view RDS Security Groups */
  public get rds_openSecurityGroups(): Metric<RdsOpenSecurityGroups> {
    return this.getMetric("rds_openSecurityGroups");
  }

  /** Open a window to view RDS Subnet Groups */
  public get rds_openSubnets(): Metric<RdsOpenSubnets> {
    return this.getMetric("rds_openSubnets");
  }

  /** Launch a RDS DB instance */
  public get rds_launchInstance(): Metric<RdsLaunchInstance> {
    return this.getMetric("rds_launchInstance");
  }

  /** Create a RDS security group */
  public get rds_createSecurityGroup(): Metric<RdsCreateSecurityGroup> {
    return this.getMetric("rds_createSecurityGroup");
  }

  /** Create a RDS subnet group */
  public get rds_createSubnetGroup(): Metric<RdsCreateSubnetGroup> {
    return this.getMetric("rds_createSubnetGroup");
  }

  /** Delete a RDS DB instance */
  public get rds_deleteInstance(): Metric<RdsDeleteInstance> {
    return this.getMetric("rds_deleteInstance");
  }

  /** Delete RDS security group(s) */
  public get rds_deleteSecurityGroup(): Metric<RdsDeleteSecurityGroup> {
    return this.getMetric("rds_deleteSecurityGroup");
  }

  /** Delete RDS subnet group(s) */
  public get rds_deleteSubnetGroup(): Metric<RdsDeleteSubnetGroup> {
    return this.getMetric("rds_deleteSubnetGroup");
  }

  /** Called when creating a new database connection configuration to for a RDS database. In Datagrip we do not get this infromation if it is created directly, so this is only counts actions. */
  public get rds_createConnectionConfiguration(): Metric<RdsCreateConnectionConfiguration> {
    return this.getMetric("rds_createConnectionConfiguration");
  }

  /** Called when getting IAM/SecretsManager credentials for a Redshift database. Value represents how long it takes in ms. */
  public get redshift_getCredentials(): Metric<RedshiftGetCredentials> {
    return this.getMetric("redshift_getCredentials");
  }

  /** Called when creating a new database connection configuration to for a Redshift database. In Datagrip we do not get this infromation if it is created directly, so this only counts actions. */
  public get redshift_createConnectionConfiguration(): Metric<RedshiftCreateConnectionConfiguration> {
    return this.getMetric("redshift_createConnectionConfiguration");
  }

  /** Called when deploying a SAM application */
  public get sam_deploy(): Metric<SamDeploy> {
    return this.getMetric("sam_deploy");
  }

  /** Called when syncing a SAM application */
  public get sam_sync(): Metric<SamSync> {
    return this.getMetric("sam_sync");
  }

  /** Called when initing a SAM application */
  public get sam_init(): Metric<SamInit> {
    return this.getMetric("sam_init");
  }

  /** Called when selecting an EventBridge schema to view */
  public get schemas_view(): Metric<SchemasView> {
    return this.getMetric("schemas_view");
  }

  /** Called when downloading an EventBridge schema */
  public get schemas_download(): Metric<SchemasDownload> {
    return this.getMetric("schemas_download");
  }

  /** Called when searching an EventBridge schema registry */
  public get schemas_search(): Metric<SchemasSearch> {
    return this.getMetric("schemas_search");
  }

  /** Called when starting the plugin */
  public get session_start(): Metric<SessionStart> {
    return this.getMetric("session_start");
  }

  /** Called when stopping the IDE on a best effort basis */
  public get session_end(): Metric<SessionEnd> {
    return this.getMetric("session_end");
  }

  /** Copy the bucket name to the clipboard */
  public get s3_copyBucketName(): Metric<S3CopyBucketName> {
    return this.getMetric("s3_copyBucketName");
  }

  /** Copy the path of a S3 object to the clipboard */
  public get s3_copyPath(): Metric<S3CopyPath> {
    return this.getMetric("s3_copyPath");
  }

  /** Copy the S3 URI of a S3 object to the clipboard (e.g. s3://<bucketName>/abc.txt) */
  public get s3_copyUri(): Metric<S3CopyUri> {
    return this.getMetric("s3_copyUri");
  }

  /** Copy the URL of a S3 object to the clipboard */
  public get s3_copyUrl(): Metric<S3CopyUrl> {
    return this.getMetric("s3_copyUrl");
  }

  /** Create a S3 bucket */
  public get s3_createBucket(): Metric<S3CreateBucket> {
    return this.getMetric("s3_createBucket");
  }

  /** Delete a S3 bucket */
  public get s3_deleteBucket(): Metric<S3DeleteBucket> {
    return this.getMetric("s3_deleteBucket");
  }

  /** Delete S3 object(s) */
  public get s3_deleteObject(): Metric<S3DeleteObject> {
    return this.getMetric("s3_deleteObject");
  }

  /** Create an S3 folder */
  public get s3_createFolder(): Metric<S3CreateFolder> {
    return this.getMetric("s3_createFolder");
  }

  /** Download S3 object(s) */
  public get s3_downloadObject(): Metric<S3DownloadObject> {
    return this.getMetric("s3_downloadObject");
  }

  /** Download multiple S3 objects */
  public get s3_downloadObjects(): Metric<S3DownloadObjects> {
    return this.getMetric("s3_downloadObjects");
  }

  /** Upload S3 object(s) */
  public get s3_uploadObject(): Metric<S3UploadObject> {
    return this.getMetric("s3_uploadObject");
  }

  /** Rename a single S3 object */
  public get s3_renameObject(): Metric<S3RenameObject> {
    return this.getMetric("s3_renameObject");
  }

  /** Upload multiple S3 objects */
  public get s3_uploadObjects(): Metric<S3UploadObjects> {
    return this.getMetric("s3_uploadObjects");
  }

  /** Open a view of a S3 bucket */
  public get s3_openEditor(): Metric<S3OpenEditor> {
    return this.getMetric("s3_openEditor");
  }

  /** Edit or view one or more S3 objects in the IDE */
  public get s3_editObject(): Metric<S3EditObject> {
    return this.getMetric("s3_editObject");
  }

  /** Open a window to view S3 bucket properties */
  public get s3_openBucketProperties(): Metric<S3OpenBucketProperties> {
    return this.getMetric("s3_openBucketProperties");
  }

  /** Open a window to view S3 Multipart upload */
  public get s3_openMultipartUpload(): Metric<S3OpenMultipartUpload> {
    return this.getMetric("s3_openMultipartUpload");
  }

  /** The Toolkit has completed initialization */
  public get toolkit_init(): Metric<ToolkitInit> {
    return this.getMetric("toolkit_init");
  }

  /** View logs for the toolkit */
  public get toolkit_viewLogs(): Metric<ToolkitViewLogs> {
    return this.getMetric("toolkit_viewLogs");
  }

  /** Open an SQS queue. Initially opens to either the send message pane or poll messages pane. */
  public get sqs_openQueue(): Metric<SqsOpenQueue> {
    return this.getMetric("sqs_openQueue");
  }

  /** Create a new SQS queue */
  public get sqs_createQueue(): Metric<SqsCreateQueue> {
    return this.getMetric("sqs_createQueue");
  }

  /** Send a message to an SQS queue */
  public get sqs_sendMessage(): Metric<SqsSendMessage> {
    return this.getMetric("sqs_sendMessage");
  }

  /** Delete one or more messages from an SQS queue. Value indicates the number of messages that we tried to delete. */
  public get sqs_deleteMessages(): Metric<SqsDeleteMessages> {
    return this.getMetric("sqs_deleteMessages");
  }

  /** Subscribe the queue to messages from an sns topic */
  public get sqs_subscribeSns(): Metric<SqsSubscribeSns> {
    return this.getMetric("sqs_subscribeSns");
  }

  /** Configure the queue as a trigger for a Lambda */
  public get sqs_configureLambdaTrigger(): Metric<SqsConfigureLambdaTrigger> {
    return this.getMetric("sqs_configureLambdaTrigger");
  }

  /** Edit the Queue parameters */
  public get sqs_editQueueParameters(): Metric<SqsEditQueueParameters> {
    return this.getMetric("sqs_editQueueParameters");
  }

  /** Purge all messages from the queue */
  public get sqs_purgeQueue(): Metric<SqsPurgeQueue> {
    return this.getMetric("sqs_purgeQueue");
  }

  /** Called when user deletes a SQS queue */
  public get sqs_deleteQueue(): Metric<SqsDeleteQueue> {
    return this.getMetric("sqs_deleteQueue");
  }

  /** Create a SNS Topic */
  public get sns_createTopic(): Metric<SnsCreateTopic> {
    return this.getMetric("sns_createTopic");
  }

  /** Create a SNS Subscription */
  public get sns_createSubscription(): Metric<SnsCreateSubscription> {
    return this.getMetric("sns_createSubscription");
  }

  /** Open a window to view details of SNS Topic */
  public get sns_openTopic(): Metric<SnsOpenTopic> {
    return this.getMetric("sns_openTopic");
  }

  /** Open a window to view SNS Subscriptions */
  public get sns_openSubscriptions(): Metric<SnsOpenSubscriptions> {
    return this.getMetric("sns_openSubscriptions");
  }

  /** Called when user deletes a SNS Topic */
  public get sns_deleteTopic(): Metric<SnsDeleteTopic> {
    return this.getMetric("sns_deleteTopic");
  }

  /** Called when user deletes SNS subscription(s) */
  public get sns_deleteSubscription(): Metric<SnsDeleteSubscription> {
    return this.getMetric("sns_deleteSubscription");
  }

  /** Publish message to a SNS topic */
  public get sns_publishMessage(): Metric<SnsPublishMessage> {
    return this.getMetric("sns_publishMessage");
  }

  /** Open a window to view VPC RouteTable */
  public get vpc_openRouteTables(): Metric<VpcOpenRouteTables> {
    return this.getMetric("vpc_openRouteTables");
  }

  /** Open a window to view VPC Internet Gateway */
  public get vpc_openGateways(): Metric<VpcOpenGateways> {
    return this.getMetric("vpc_openGateways");
  }

  /** Open a window to view VPC Network ACLs */
  public get vpc_openACLs(): Metric<VpcOpenACLs> {
    return this.getMetric("vpc_openACLs");
  }

  /** Open a window to view VPC Subnets */
  public get vpc_openSubnets(): Metric<VpcOpenSubnets> {
    return this.getMetric("vpc_openSubnets");
  }

  /** Open a window to view VPC details */
  public get vpc_openVPCs(): Metric<VpcOpenVPCs> {
    return this.getMetric("vpc_openVPCs");
  }

  /** Open the insights query editor */
  public get cloudwatchinsights_openEditor(): Metric<CloudwatchinsightsOpenEditor> {
    return this.getMetric("cloudwatchinsights_openEditor");
  }

  /** Start an insights query */
  public get cloudwatchinsights_executeQuery(): Metric<CloudwatchinsightsExecuteQuery> {
    return this.getMetric("cloudwatchinsights_executeQuery");
  }

  /** Save query parameters to AWS */
  public get cloudwatchinsights_saveQuery(): Metric<CloudwatchinsightsSaveQuery> {
    return this.getMetric("cloudwatchinsights_saveQuery");
  }

  /** Retrieve list of available saved queries from AWS */
  public get cloudwatchinsights_retrieveQuery(): Metric<CloudwatchinsightsRetrieveQuery> {
    return this.getMetric("cloudwatchinsights_retrieveQuery");
  }

  /** Get all details for the selected log record */
  public get cloudwatchinsights_openDetailedLogRecord(): Metric<CloudwatchinsightsOpenDetailedLogRecord> {
    return this.getMetric("cloudwatchinsights_openDetailedLogRecord");
  }

  /** The toolkit tried to retrieve blob data from a url */
  public get toolkit_getExternalResource(): Metric<ToolkitGetExternalResource> {
    return this.getMetric("toolkit_getExternalResource");
  }

  /** Open the dynamic resource model in the IDE */
  public get dynamicresource_getResource(): Metric<DynamicresourceGetResource> {
    return this.getMetric("dynamicresource_getResource");
  }

  /** Expand a Resource Type node */
  public get dynamicresource_listResource(): Metric<DynamicresourceListResource> {
    return this.getMetric("dynamicresource_listResource");
  }

  /** Change the list of available dynamic resources in the AWS Explorer */
  public get dynamicresource_selectResources(): Metric<DynamicresourceSelectResources> {
    return this.getMetric("dynamicresource_selectResources");
  }

  /** Copy the dynamic resource identifier */
  public get dynamicresource_copyIdentifier(): Metric<DynamicresourceCopyIdentifier> {
    return this.getMetric("dynamicresource_copyIdentifier");
  }

  /** A dynamic resource mutation request completed */
  public get dynamicresource_mutateResource(): Metric<DynamicresourceMutateResource> {
    return this.getMetric("dynamicresource_mutateResource");
  }

  /** An experiment was activated or deactivated in the Toolkit */
  public get aws_experimentActivation(): Metric<AwsExperimentActivation> {
    return this.getMetric("aws_experimentActivation");
  }

  /** An external tool was installed automatically */
  public get aws_toolInstallation(): Metric<AwsToolInstallation> {
    return this.getMetric("aws_toolInstallation");
  }

  /** An setting was changed by users in the Toolkit. This metric can optionally provide the new state of the setting via settingState. */
  public get aws_modifySetting(): Metric<AwsModifySetting> {
    return this.getMetric("aws_modifySetting");
  }

  /** User clicked/activated a UI element. This does not necessarily have to be an explicit mouse click. Any user action that has the same behavior as a mouse click can use this event. */
  public get ui_click(): Metric<UiClick> {
    return this.getMetric("ui_click");
  }

  /** User requested that a resource be opened in the browser using the deeplink service */
  public get deeplink_open(): Metric<DeeplinkOpen> {
    return this.getMetric("deeplink_open");
  }

  /** Percentage of user tokens against suggestions until 5 mins of time */
  public get codewhisperer_codePercentage(): Metric<CodewhispererCodePercentage> {
    return this.getMetric("codewhisperer_codePercentage");
  }

  /** Client side invocation of the CodeWhisperer Security Scan */
  public get codewhisperer_securityScan(): Metric<CodewhispererSecurityScan> {
    return this.getMetric("codewhisperer_securityScan");
  }

  /** Client side invocation of the CodeWhisperer service for suggestion */
  public get codewhisperer_serviceInvocation(): Metric<CodewhispererServiceInvocation> {
    return this.getMetric("codewhisperer_serviceInvocation");
  }

  /** Client side invocation blocked by another invocation in progress */
  public get codewhisperer_blockedInvocation(): Metric<CodewhispererBlockedInvocation> {
    return this.getMetric("codewhisperer_blockedInvocation");
  }

  /** User acceptance or rejection of each suggestion returned by the CodeWhisperer service request */
  public get codewhisperer_userDecision(): Metric<CodewhispererUserDecision> {
    return this.getMetric("codewhisperer_userDecision");
  }

  /** User decision aggregated at trigger level */
  public get codewhisperer_userTriggerDecision(): Metric<CodewhispererUserTriggerDecision> {
    return this.getMetric("codewhisperer_userTriggerDecision");
  }

  /** Percentage of user modifications for the selected suggestion until a fixed period of time */
  public get codewhisperer_userModification(): Metric<CodewhispererUserModification> {
    return this.getMetric("codewhisperer_userModification");
  }

  /** The duration from user last modification to the first recommendation shown in milliseconds */
  public get codewhisperer_perceivedLatency(): Metric<CodewhispererPerceivedLatency> {
    return this.getMetric("codewhisperer_perceivedLatency");
  }

  /** The latency from each CodeWhisperer components in milliseconds */
  public get codewhisperer_clientComponentLatency(): Metric<CodewhispererClientComponentLatency> {
    return this.getMetric("codewhisperer_clientComponentLatency");
  }

  /** Create an Amazon CodeCatalyst Dev Environment */
  public get codecatalyst_createDevEnvironment(): Metric<CodecatalystCreateDevEnvironment> {
    return this.getMetric("codecatalyst_createDevEnvironment");
  }

  /** Update properties of a Amazon CodeCatalyst Dev Environment */
  public get codecatalyst_updateDevEnvironmentSettings(): Metric<CodecatalystUpdateDevEnvironmentSettings> {
    return this.getMetric("codecatalyst_updateDevEnvironmentSettings");
  }

  /** Trigger a devfile update on a Amazon CodeCatalyst dev environment */
  public get codecatalyst_updateDevfile(): Metric<CodecatalystUpdateDevfile> {
    return this.getMetric("codecatalyst_updateDevfile");
  }

  /** Clone a Amazon CodeCatalyst code repository locally */
  public get codecatalyst_localClone(): Metric<CodecatalystLocalClone> {
    return this.getMetric("codecatalyst_localClone");
  }

  /** Connect to a Amazon CodeCatalyst dev environment */
  public get codecatalyst_connect(): Metric<CodecatalystConnect> {
    return this.getMetric("codecatalyst_connect");
  }

  /** Workflow statistic for connecting to a dev environment */
  public get codecatalyst_devEnvironmentWorkflowStatistic(): Metric<CodecatalystDevEnvironmentWorkflowStatistic> {
    return this.getMetric("codecatalyst_devEnvironmentWorkflowStatistic");
  }

  /** Emitted whenever a registered Toolkit command is executed */
  public get vscode_executeCommand(): Metric<VscodeExecuteCommand> {
    return this.getMetric("vscode_executeCommand");
  }

  /** An SSM Document is created locally */
  public get ssm_createDocument(): Metric<SsmCreateDocument> {
    return this.getMetric("ssm_createDocument");
  }

  /** An SSM Document is deleted */
  public get ssm_deleteDocument(): Metric<SsmDeleteDocument> {
    return this.getMetric("ssm_deleteDocument");
  }

  /** An SSM Document is deleted */
  public get ssm_executeDocument(): Metric<SsmExecuteDocument> {
    return this.getMetric("ssm_executeDocument");
  }

  /** An SSM Document is opened locally */
  public get ssm_openDocument(): Metric<SsmOpenDocument> {
    return this.getMetric("ssm_openDocument");
  }

  /** SSM Document related metrics for create and update */
  public get ssm_publishDocument(): Metric<SsmPublishDocument> {
    return this.getMetric("ssm_publishDocument");
  }

  /** SSM Document related metrics for updating document default version */
  public get ssm_updateDocumentVersion(): Metric<SsmUpdateDocumentVersion> {
    return this.getMetric("ssm_updateDocumentVersion");
  }

  /** */
  public get stepfunctions_createStateMachineFromTemplate(): Metric<StepfunctionsCreateStateMachineFromTemplate> {
    return this.getMetric("stepfunctions_createStateMachineFromTemplate");
  }

  /** */
  public get stepfunctions_downloadStateMachineDefinition(): Metric<StepfunctionsDownloadStateMachineDefinition> {
    return this.getMetric("stepfunctions_downloadStateMachineDefinition");
  }

  /** */
  public get stepfunctions_executeStateMachine(): Metric<StepfunctionsExecuteStateMachine> {
    return this.getMetric("stepfunctions_executeStateMachine");
  }

  /** */
  public get stepfunctions_executeStateMachineView(): Metric<StepfunctionsExecuteStateMachineView> {
    return this.getMetric("stepfunctions_executeStateMachineView");
  }

  /** */
  public get stepfunctions_previewstatemachine(): Metric<StepfunctionsPreviewstatemachine> {
    return this.getMetric("stepfunctions_previewstatemachine");
  }

  /** Record the number of active regions at startup and when regions are added/removed */
  public get vscode_activeRegions(): Metric<VscodeActiveRegions> {
    return this.getMetric("vscode_activeRegions");
  }

  /** View the VSCode IDE logs */
  public get vscode_viewLogs(): Metric<VscodeViewLogs> {
    return this.getMetric("vscode_viewLogs");
  }

  /** Called when getting more details about errors thrown by the explorer */
  public get aws_showExplorerErrorDetails(): Metric<AwsShowExplorerErrorDetails> {
    return this.getMetric("aws_showExplorerErrorDetails");
  }

  /** Records a call to add a region to the explorer */
  public get aws_showRegion(): Metric<AwsShowRegion> {
    return this.getMetric("aws_showRegion");
  }

  /** Records a call to remove a region from the explorer */
  public get aws_hideRegion(): Metric<AwsHideRegion> {
    return this.getMetric("aws_hideRegion");
  }

  /** Called when detecting the location of the SAM CLI */
  public get sam_detect(): Metric<SamDetect> {
    return this.getMetric("sam_detect");
  }

  /** Called when expanding the CDK explorer is disabled */
  public get cdk_explorerDisabled(): Metric<CdkExplorerDisabled> {
    return this.getMetric("cdk_explorerDisabled");
  }

  /** Called when the CDK explorer is enabled */
  public get cdk_explorerEnabled(): Metric<CdkExplorerEnabled> {
    return this.getMetric("cdk_explorerEnabled");
  }

  /** Called when the CDK explorer is expanded */
  public get cdk_appExpanded(): Metric<CdkAppExpanded> {
    return this.getMetric("cdk_appExpanded");
  }

  /** Called when providing feedback for CDK */
  public get cdk_provideFeedback(): Metric<CdkProvideFeedback> {
    return this.getMetric("cdk_provideFeedback");
  }

  /** Called when clicking on help for CDK */
  public get cdk_help(): Metric<CdkHelp> {
    return this.getMetric("cdk_help");
  }

  /** Called when refreshing the CDK explorer */
  public get cdk_refreshExplorer(): Metric<CdkRefreshExplorer> {
    return this.getMetric("cdk_refreshExplorer");
  }

  /** Called after trying to attach a debugger to a local sam invoke */
  public get sam_attachDebugger(): Metric<SamAttachDebugger> {
    return this.getMetric("sam_attachDebugger");
  }

  /** Called after opening the SAM Config UI */
  public get sam_openConfigUi(): Metric<SamOpenConfigUi> {
    return this.getMetric("sam_openConfigUi");
  }

  protected abstract getMetric(name: string): Metric;
}
