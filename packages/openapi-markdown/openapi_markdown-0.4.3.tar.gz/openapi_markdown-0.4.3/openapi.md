# SuperAging Server API

API Documentation

# Base URL


| URL | Description |
|-----|-------------|
| / | Local Server |


# Authentication



## Security Schemes

| Name              | Type              | Description              | Scheme              | Bearer Format             |
|-------------------|-------------------|--------------------------|---------------------|---------------------------|
| jwt | http |  | bearer | JWT |

# APIs

# Components



## TermsSimpleDto



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| title | string |  |
| url | string |  |
| agreed | boolean | null 이면, 아직 동의 안함. |


## UserSettings


사용자 모델


| Field | Type | Description |
|-------|------|-------------|
| reminderHour | integer |  |
| lastReminderHour | integer |  |
| reminderUpdatedAt | string |  |
| defaultReminderHour | integer |  |
| remindBufferMinutes | integer |  |
| remindChangeDays | integer |  |
| recallAnyTime | boolean |  |
| treatmentAnyTime | boolean | true 이면, treatment.availableHours 을 무시하고 언제든지 테스트 가능 |
| baseUrls | array |  |
| terms | array |  |


## ResponseUserClientResponse



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## UserClientResponse


사용자 모델


| Field | Type | Description |
|-------|------|-------------|
| account | string |  |
| settings |  |  |
| passwordChangeRequired | boolean |  |
| name | string |  |
| sex | integer |  |
| age | integer |  |


## PasswordUpdateRequest



| Field | Type | Description |
|-------|------|-------------|
| password | string |  |


## PrescriptionModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| title | string |  |


## ResponseUserModel



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## SelectOption


선택 옵션


| Field | Type | Description |
|-------|------|-------------|
| value | object | 선택 값 |
| label | string | 사용자에게 보여질 라벨 |


## UserModel


사용자 모델


| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| account | string |  |
| name | string |  |
| mobileNumber | string |  |
| status | string |  |
| passwordChangeRequired | boolean |  |
| settings |  |  |
| prescriptionId | integer |  |
| userPrescription |  |  |
| sex |  |  |
| birthYear | integer |  |
| createdAt | string |  |


## UserPrescriptionModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| prescription |  |  |
| prescribedAt | string |  |
| startedAt | string |  |
| endedAt | string |  |
| currentRound | integer |  |
| totalRound | integer |  |
| status | string |  |
| lastRound | integer |  |


## LoginRefreshRequest



| Field | Type | Description |
|-------|------|-------------|
| refreshToken | string |  |


## LoginResponseModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| account | string |  |
| accessToken | string |  |
| refreshToken | string |  |


## Answer



| Field | Type | Description |
|-------|------|-------------|
| input | string |  |
| options | array |  |


## ContentProgress



| Field | Type | Description |
|-------|------|-------------|
| contentId | integer |  |
| progress | integer |  |


## DiseaseRecord





## ExerciseMonitoringEventValue





## ExerciseRecord





## GameRecord





## NutritionRecord





## PushMessageEventValue





## RecallAnswer



| Field | Type | Description |
|-------|------|-------------|
| value | string |  |
| correct | boolean |  |
| hintIndex | integer |  |
| type | string |  |


## RecallRecord





## SurveyRecord





## TreatmentRecord



| Field | Type | Description |
|-------|------|-------------|
| type | string |  |


## TreatmentUpdateEventValue





## TreatmentUpdateModel



| Field | Type | Description |
|-------|------|-------------|
| status | string | 미래 기억과제에서 등록 (0) => 확인 (1) 의 상태를 처리하기위한 상태값, 필요에 따라 다른 과제에서도 사용 가능성이 있어 보임. |
| data |  |  |
| sessionId | integer |  |


## ResponseUserSessionResponse



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## UserSessionResponse



| Field | Type | Description |
|-------|------|-------------|
| sessionId | integer |  |


## ResponseListUserTag



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload | array |  |


## UserTag


선택 옵션


| Field | Type | Description |
|-------|------|-------------|
| code | string |  |
| name | string |  |
| value |  |  |


## EmptyPayload





## ResponseEmptyPayload



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## ChangePasswordModel



| Field | Type | Description |
|-------|------|-------------|
| changePasswordToken | string |  |
| account | string |  |
| password | string |  |
| newPassword | string |  |


## ResponseString



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload | string |  |


## TermsAgreementDto



| Field | Type | Description |
|-------|------|-------------|
| termsId | integer |  |
| agreed | boolean |  |


## CalorieRecordData





## HealthDataModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| recordedAt | integer |  |
| device | string |  |
| dataOrigin | string |  |
| clientRecordId | string |  |
| data |  |  |


## HealthRecordData



| Field | Type | Description |
|-------|------|-------------|
| time | integer |  |
| @type | string |  |


## HeartRateRecordData





## SleepStageRecordData





## StepRecordData





## DeviceModel



| Field | Type | Description |
|-------|------|-------------|
| uuid | string |  |
| type | string |  |
| pushToken | string |  |


## LoginModel



| Field | Type | Description |
|-------|------|-------------|
| account | string |  |
| password | string |  |


## AppEventDto


App event client data transfer object


| Field | Type | Description |
|-------|------|-------------|
| sessionId | integer |  |
| eventTime | integer |  |
| processingId | string | The same id should be processed at the same time |
| value |  |  |


## AppEventRequest



| Field | Type | Description |
|-------|------|-------------|
| events | array |  |


## AppDeployModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| packageName | string |  |
| versionCode | integer |  |
| storePlatform | string |  |
| version | string |  |
| url | string |  |
| deployedAt | string |  |


## ResponseAppDeployModel



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## UserCreateRequest


사용자 생성 모델


| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| account | string |  |
| name | string |  |
| mobileNumber | string |  |
| status | string |  |
| sex |  |  |
| birthYear | integer |  |
| createdAt | string |  |


## TermsModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| title | string |  |
| contentType | string |  |
| content | string |  |
| target | string |  |
| required | boolean |  |
| effectiveAt | string |  |


## ResponseBoolean



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload | boolean |  |


## ImageRequestModel



| Field | Type | Description |
|-------|------|-------------|
| model | string |  |
| prompt | string |  |
| n | integer |  |
| responseFormat | string |  |
| size | string |  |


## ImageResponse



| Field | Type | Description |
|-------|------|-------------|
| data | array |  |


## ResponseData



| Field | Type | Description |
|-------|------|-------------|
| url | string |  |
| b64_json | string |  |


## ResponseImageResponse



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## UserEnrollRequest



| Field | Type | Description |
|-------|------|-------------|
| name | string |  |
| mobileNumber | string |  |
| prescriptionId | integer |  |


## ResponseUserEnrollResponse



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## UserEnrollResponse



| Field | Type | Description |
|-------|------|-------------|
| mobileNumber | string |  |
| passcode | string |  |
| expiredAt | string |  |


## ResetPasswordModel



| Field | Type | Description |
|-------|------|-------------|
| account | string |  |
| email | string |  |


## ResponseLoginResponseModel



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## AdminUserDto



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| account | string |  |
| name | string |  |
| email | string |  |
| createdAt | string |  |
| password | string |  |


## ResponseAdminUserDto



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## DiseaseConfiguration





## ExerciseConfiguration





## GameConfiguration





## NutritionConfiguration





## QuestionModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| code | string |  |
| query | string |  |
| type | string |  |
| options | array |  |
| hideExpr | string |  |
| optional | boolean |  |


## QuestionOptionModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| text | string |  |
| value | number |  |


## RecallConfiguration





## RecallHint



| Field | Type | Description |
|-------|------|-------------|
| type | string |  |
| options | array |  |
| text | string |  |


## ResponseTreatmentRoundModel



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## SurveyConfiguration





## TreatmentConfiguration



| Field | Type | Description |
|-------|------|-------------|
| type | string |  |


## TreatmentContent



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| code | string |  |
| uri | string |  |
| title | string |  |
| value | string |  |
| category | string |  |
| priority | integer |  |
| playSeconds | integer |  |
| checksum | string |  |


## TreatmentModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| title | string |  |
| summary | string |  |
| priority | integer |  |
| previewUrl | string |  |
| type | string |  |
| availableDate | string |  |
| availableHours | array |  |
| configuration |  |  |
| contents | array |  |
| round | integer |  |
| status | string | 미래 기억과제에서 등록 (0) => 확인 (1) 의 상태를 처리하기위한 상태값, 필요에 따라 다른 과제에서도 사용 가능성이 있어 보임. |
| data |  |  |
| lastSession | integer |  |


## TreatmentRoundModel



| Field | Type | Description |
|-------|------|-------------|
| prescription |  |  |
| treatments | array |  |
| updated | boolean |  |


## WarningCard



| Field | Type | Description |
|-------|------|-------------|
| title | string |  |
| content | string |  |
| uri | string |  |
| index | integer |  |


## Pageable



| Field | Type | Description |
|-------|------|-------------|
| page | integer |  |
| size | integer |  |
| sort | array |  |


## DataColumn


react-table column definition


| Field | Type | Description |
|-------|------|-------------|
| accessor | string |  |
| width | string |  |
| Header | string |  |


## ListResponseUserModel



| Field | Type | Description |
|-------|------|-------------|
| columns | array |  |
| rows | array |  |
| page | integer |  |
| pageSize | integer |  |
| totalElements | integer |  |


## ResponseListResponseUserModel



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## ListResponseUserTreatmentResult



| Field | Type | Description |
|-------|------|-------------|
| columns | array |  |
| rows | array |  |
| page | integer |  |
| pageSize | integer |  |
| totalElements | integer |  |


## ResponseListResponseUserTreatmentResult



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## UserTreatmentResult



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| round | integer |  |
| type | string |  |
| domain | string |  |
| title | string |  |
| metric1 | number |  |
| state | string |  |
| availableDate | string |  |
| startedAt | string |  |


## ResponseUserTreatmentResultDetail



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## TreatmentDetailItem



| Field | Type | Description |
|-------|------|-------------|
| category | string |  |
| span | integer |  |
| label | string |  |
| value |  |  |
| value2 | object |  |


## TypedValue



| Field | Type | Description |
|-------|------|-------------|
| type | string |  |
| value | object |  |


## UserContentResult



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| category | string |  |
| title | string |  |
| progress | number |  |
| metric1 | number |  |
| leastActionCount | integer |  |
| positiveActionCount | integer |  |
| negativeActionCount | integer |  |
| playPositionMs | integer |  |
| totalPlayedMs | integer |  |
| durationMs | integer |  |
| startedAt | string |  |
| finishedAt | string |  |


## UserTreatmentResultDetail



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| title | string |  |
| startedAt | string |  |
| finishedAt | string |  |
| metric1 | number |  |
| progress | number |  |
| type | string |  |
| status | string |  |
| results | array |  |
| configuration |  |  |
| record |  |  |
| detailItems | array |  |


## ResponseSurveyResult



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## SurveyResult



| Field | Type | Description |
|-------|------|-------------|
| title | string |  |
| description | string |  |
| questions | array |  |
| answerMap | object |  |


## ListResponseUserTreatmentSessionSimple



| Field | Type | Description |
|-------|------|-------------|
| columns | array |  |
| rows | array |  |
| page | integer |  |
| pageSize | integer |  |
| totalElements | integer |  |


## ResponseListResponseUserTreatmentSessionSimple



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## UserTreatmentSessionSimple



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| clientSessionId | integer | 단말에서 생성하는 세션 아이디.
 오프라인의 경우 서버에서 세션 아이디를 생성할 수 없기 때문에 단말의 세션 아이디는 반드시 필요하게 된다. |
| sessionType | string |  |
| status | string |  |
| startedAt | string |  |
| finishedAt | string |  |
| metric1 | number |  |


## AppEventModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| userId | integer |  |
| sessionId | integer |  |
| eventTime | integer |  |
| processingId | string |  |
| value |  |  |
| status | string |  |


## ResponseUserTreatmentSessionData



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## UserTreatmentSessionData



| Field | Type | Description |
|-------|------|-------------|
| events | array |  |


## ResponseListUserProgressSummary



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload | array |  |


## UserProgressSummary



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| account | string |  |
| name | string |  |
| mobileNumber | string |  |
| progress | number |  |
| totalCount | integer |  |


## DomainProgressChartData



| Field | Type | Description |
|-------|------|-------------|
| labels | array |  |
| data | array |  |


## ResponseRoundStatSummary



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## RoundStatSummary



| Field | Type | Description |
|-------|------|-------------|
| round | integer |  |
| week | integer |  |
| weekRound | integer |  |
| hasNextRound | boolean |  |
| hasPrevRound | boolean |  |
| totalProgress | number |  |
| chartData |  |  |


## ListResponseTermsModel



| Field | Type | Description |
|-------|------|-------------|
| columns | array |  |
| rows | array |  |
| page | integer |  |
| pageSize | integer |  |
| totalElements | integer |  |


## ResponseListPrescriptionModel



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload | array |  |


## ContentModel



| Field | Type | Description |
|-------|------|-------------|
| id | integer |  |
| treatmentId | integer |  |
| code | string |  |
| uri | string |  |
| title | string |  |
| playSeconds | integer | 컨텐츠의 플레이 시간, 동영상의 경우 동영상 재생시간, 게임의 경우 게임 타임아웃. |
| variationCount | integer | 일반적으로 해당 컨텐츠가 세부적으로 여러 종류로 나뉠때, 그 종류의 수를 나타낸다. Game 컨텐츠에서는 레벨수를 나타낸다. |
| value | string |  |
| category | string |  |
| priority | integer |  |
| checksum | string |  |


## ListResponseContentModel



| Field | Type | Description |
|-------|------|-------------|
| columns | array |  |
| rows | array |  |
| page | integer |  |
| pageSize | integer |  |
| totalElements | integer |  |


## ResponseListResponseContentModel



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |


## ListResponseAdminUserDto



| Field | Type | Description |
|-------|------|-------------|
| columns | array |  |
| rows | array |  |
| page | integer |  |
| pageSize | integer |  |
| totalElements | integer |  |


## ResponseListResponseAdminUserDto



| Field | Type | Description |
|-------|------|-------------|
| status | integer |  |
| payload |  |  |
