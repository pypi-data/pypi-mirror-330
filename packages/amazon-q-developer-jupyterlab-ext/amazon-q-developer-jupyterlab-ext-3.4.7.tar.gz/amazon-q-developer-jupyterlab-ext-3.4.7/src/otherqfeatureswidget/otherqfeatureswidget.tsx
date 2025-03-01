import React, { useEffect, useState } from 'react';
import { Box } from '@mui/system';
import {
    Alert,
    Button,
    FormControl,
    InputLabel,
    MenuItem,
    Select,
    ThemeProvider,
} from '@mui/material';
import { ApiClient } from '../client/apiclient';
import { ReactWidget } from '@jupyterlab/apputils';
import { createDirectoryIfDoesNotExist, readFile, saveFile } from '../utils/utils';
import { AMAZON_Q_DIRECTORY, AuthMode, AWS_DIRECTORY } from '../utils/constants';
import { pageDisplayStyle, saveButtonStyle } from './styles';
import { Application } from '../application';
import { getJupyterLabTheme } from '../utils/getJupyterLabTheme';

type Customization = {
	arn: string,
	name?: string,
    description?: string
}

enum AlertType {
    Success = 'success',
    Error = 'error',
    Warning = 'warning',
    None = 'none'
}

const AlertMessages = {
  success: 'Successfully saved changes!',
  saveCustomizationError: 'Failed to save customization in ~/.aws/amazon_q/customization_arn.json',
  loadCustomizationError: 'Failed to find current customization. Please make sure customization_arn is correct at ~/.aws/amazon_q/customization_arn.json',
  fetchCustomizationError: 'Error in getting all available customizations:',
  noSubscriptionError: 'Customization is only supported in Amazon Q Developer Pro Tier.'
}

const CUSTOMIZATION_HEADER = "Select Customization";
const CUSTOMIZATION_DESCRIPTION = "Q developer customizations lets you tailor code suggestions using your team's internal libraries, proprietary techniques and enterprise coding style.";

const NO_VALUE = "No value";
const ARN_FILE_NAME = "customization_arn"

const OtherQFeatures: React.FunctionComponent = () => {
    const [customization, setCustomization] = useState<string>(NO_VALUE);
    const [allCustomizations, setAllCustomizations] = useState<Customization[]>([]);

    const [saving, setSaving] = useState<boolean>(false);
    const [alert, setAlert] = useState<AlertType>(AlertType.None);
    const [alertMessage, setAlertMessage] = useState<string>('');
    const [authMode, setAuthMode] = useState<AuthMode>(AuthMode.SSO);

    useEffect(() => {
        const fetchCurrentCustomization = async () => {
            // retrieve customization in use
            try {
                await createDirectoryIfDoesNotExist(AWS_DIRECTORY, '.aws');
                await createDirectoryIfDoesNotExist(AMAZON_Q_DIRECTORY, 'amazon_q');

                const response = await readFile(AMAZON_Q_DIRECTORY, ARN_FILE_NAME, 'json');

                // no customization if json is not found
                if (response.status === 404) return;
                const jsonData = await response.json();

                // loadCustomizationError will be displayed if json is in bad format
                const customization_arn = JSON.parse(jsonData.content).customization_arn;
                const converted_arn = customization_arn === '' ? NO_VALUE : customization_arn;
                setCustomization(converted_arn);

            } catch (error) {
                setAlert(AlertType.Error);
                setAlertMessage(AlertMessages.loadCustomizationError);
            }
        }

        const fetchAvailableCustomizations = async () => {
            try {
                const client = new ApiClient();

                const listAvailableCustomizationsResponse = await client.listAvailableCustomizations({});
                if (listAvailableCustomizationsResponse.status === "ERROR") {
                    throw Error(listAvailableCustomizationsResponse.error_info.error_message)
                }

                if (listAvailableCustomizationsResponse.data.customizations.length > 0) {
                    setAllCustomizations(listAvailableCustomizationsResponse.data.customizations);
                };
            } catch (error) {
                setAlert(AlertType.Error);
                const fetchCustomizationErrorMessage = AlertMessages.fetchCustomizationError + ' ' + String(error);
                setAlertMessage(fetchCustomizationErrorMessage);
            }
        }

        // check subscription
        const isIdcMode = Application.getInstance().isIdcMode()
        if (!isIdcMode) {
            setAuthMode(AuthMode.IAM);
            setAlert(AlertType.Warning);
            setAlertMessage(AlertMessages.noSubscriptionError);
            return;
        }

        fetchCurrentCustomization();
        fetchAvailableCustomizations();
    }, []);
    
    const isSaveButtonDisabled = () => {
        return (saving || authMode === AuthMode.IAM)
    }
    const selectCustomization: JSX.Element = (
        <>
            <h3 className="jp-ai-ChatSettings-header">{CUSTOMIZATION_HEADER}</h3>
            <FormControl fullWidth>
                <InputLabel>Available customizations</InputLabel>
                <Select
                    value={customization}
                    label="Available customizations"
                    onChange={e => {
                        setCustomization(e.target.value);
                        
                        // clear alerts
                        setAlert(AlertType.None);
                    }}
                    disabled={authMode === AuthMode.IAM}
                >
                    <MenuItem value={NO_VALUE}>No customization</MenuItem>
                    {allCustomizations.map(customization => (
                        <MenuItem value={customization.arn}>
                            {customization.name}
                        </MenuItem>
                        )
                    )}
                </Select>
                <p>{CUSTOMIZATION_DESCRIPTION}</p>
            </FormControl>
        </>
    )

    const saveCustomization = async () => {
        try {
            // Convert here since Mui select cannot have empty string as value
            const customizationArnToSave = customization === NO_VALUE ? '' : customization
            
            const response = await saveFile(AMAZON_Q_DIRECTORY, ARN_FILE_NAME, 'json', {
                customization_arn: customizationArnToSave }
            );

            if (!response.ok) {
                throw Error();
            }
        } catch (e) {
            setAlert(AlertType.Error);
            setAlertMessage(AlertMessages.saveCustomizationError)
        }
    }

    const handleSave = async () => {
        setSaving(true);

        // default to success
        setAlert(AlertType.Success);
        setAlertMessage(AlertMessages.success);

        // process saving all changes
        await saveCustomization();

        // saving state will remove old alert message banner for a short time
        // so that user would know they see the new banner
        setTimeout(() => setSaving(false), 500);
    };

    return (
        <Box sx={pageDisplayStyle}>
            {selectCustomization}
            {alert !== AlertType.None && saving === false && (
                <Alert severity={alert}>
                    {alertMessage}
                </Alert>
            )}
            <Box sx={saveButtonStyle}>
                <Button variant="contained" onClick={handleSave} disabled={isSaveButtonDisabled()}>
                    {saving ? 'Saving...' : 'Save changes'}
                </Button>
            </Box>
        </Box>
    );
}

export class OtherQFeaturesWidget extends ReactWidget {
    render(): JSX.Element {
        return (
            <ThemeProvider theme={getJupyterLabTheme()}>
                <OtherQFeatures />
            </ThemeProvider>
        );
    }
}
