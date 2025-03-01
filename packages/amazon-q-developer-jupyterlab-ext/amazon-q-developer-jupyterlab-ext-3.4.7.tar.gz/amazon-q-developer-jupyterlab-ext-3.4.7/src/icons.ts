/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { LabIcon } from '@jupyterlab/ui-components';
import codewhispererLogoSvgstr from '../style/img/qdeveloper.svg';
import codewhispererDocumentationSvgstr from '../style/img/documentation.svg';
import codewhispererReferenceLogSvgstr from '../style/img/log.svg';
import codewhispererPauseSvgstr from '../style/img/pause.svg';
import codewhispererResumeSvgstr from '../style/img/resume.svg';
import codewhispererSignOutSvgstr from '../style/img/signout.svg';
import codewhispererStartSvgstr from '../style/img/start.svg';
import visualCueArrow from '../style/img/visual-cue-arrow.svg'
import codewhispererConnectedSvgstr from '../style/img/connected.svg'
import codewhispererDisconnectedSvgstr from '../style/img/disconnected.svg'
import codewhispererLoadingSvgstr from '../style/img/loading.svg'

// TODO: Update icons to be the 16x16 icon set
export class Icons {
    static visualCueArrowIcon = new LabIcon({
        name: 'visual-cue-arrow',
        svgstr: visualCueArrow
    });

    static logoIcon = new LabIcon({
        name: 'codewhisperer:logo',
        svgstr: codewhispererLogoSvgstr
    });

    static documentationIcon = new LabIcon({
        name: 'codewhisperer:documentation',
        svgstr: codewhispererDocumentationSvgstr
    });

    static referenceLogIcon = new LabIcon({
        name: 'codewhisperer:referenceLog',
        svgstr: codewhispererReferenceLogSvgstr
    });

    static pauseIcon = new LabIcon({
        name: 'codewhisperer:pause',
        svgstr: codewhispererPauseSvgstr
    });

    static resumeIcon = new LabIcon({
        name: 'codewhisperer:resume',
        svgstr: codewhispererResumeSvgstr
    });

    static signOutIcon = new LabIcon({
        name: 'codewhisperer:signOut',
        svgstr: codewhispererSignOutSvgstr
    });

    static startIcon = new LabIcon({
        name: 'codewhisperer:start',
        svgstr: codewhispererStartSvgstr
    });

    static connectedIcon = new LabIcon({
        name: 'codewhisperer:connected',
        svgstr: codewhispererConnectedSvgstr
    });

    static disconnectedIcon = new LabIcon({
        name: 'codewhisperer:disconnected',
        svgstr: codewhispererDisconnectedSvgstr
    });

    static loadingIcon = new LabIcon({
        name: 'codewhisperer:loading',
        svgstr: codewhispererLoadingSvgstr
    })
}
